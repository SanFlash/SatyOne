from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.config import settings
from app.schemas import ExecuteIn
from app.providers.ollama_adapter import OllamaAdapter
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload
from app.db import get_db
from app.models import Category, Command, Provider, Workflow, SavedPrompt, SavedPromptVersion
from app.schemas import PromptBuildIn, PromptBuildOut, SavedPromptIn, SavedPromptOut, SavedPromptUpdateIn, SavedPromptVersionOut
from app.services.prompt_builder import build_prompt
from app.providers.openai_adapter import OpenAIAdapter

router = APIRouter()

@router.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.name).all()

@router.get("/commands")
def list_commands(
    q: str | None = None,
    category: str | None = None,
    difficulty: str | None = None,
    limit: int = Query(default=500, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    query = db.query(Command).options(joinedload(Command.category))
    if q and q.strip():
        term = f"%{q.strip()}%"
        query = query.filter(or_(
            Command.name.ilike(term),
            Command.syntax.ilike(term),
            Command.description.ilike(term),
            Command.instruction_template.ilike(term),
        ))
    if category:
        query = query.join(Category).filter(Category.slug == category)
    if difficulty:
        query = query.filter(Command.difficulty == difficulty)
    return query.order_by(Command.name).offset(offset).limit(limit).all()

@router.get("/commands/{slug}")
def get_command(slug: str, db: Session = Depends(get_db)):
    item = db.query(Command).options(joinedload(Command.category)).filter_by(slug=slug).first()
    if not item:
        raise HTTPException(status_code=404, detail="Command not found")
    return item

@router.get("/providers")
def list_providers(db: Session = Depends(get_db)):
    return db.query(Provider).order_by(Provider.name).all()

@router.get("/workflows")
def list_workflows(db: Session = Depends(get_db)):
    return db.query(Workflow).order_by(Workflow.name).all()

@router.post("/prompt-builder", response_model=PromptBuildOut)
def prompt_builder(payload: PromptBuildIn, db: Session = Depends(get_db)):
    return build_prompt(payload, db)

@router.post("/saved-prompts", response_model=SavedPromptOut)
def save_prompt(payload: SavedPromptIn, db: Session = Depends(get_db)):
    item = SavedPrompt(title=payload.title.strip(), prompt=payload.prompt, owner_key=payload.owner_key)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/saved-prompts", response_model=list[SavedPromptOut])
def get_saved_prompts(
    owner_key: str = Query(default="local-demo", min_length=1, max_length=120),
    q: str | None = Query(default=None, max_length=180),
    limit: int = Query(default=100, ge=1, le=250),
    db: Session = Depends(get_db),
):
    query = db.query(SavedPrompt).filter_by(owner_key=owner_key)
    if q and q.strip():
        term = f"%{q.strip()}%"
        query = query.filter(or_(SavedPrompt.title.ilike(term), SavedPrompt.prompt.ilike(term)))
    return query.order_by(SavedPrompt.created_at.desc()).limit(limit).all()


@router.put("/saved-prompts/{prompt_id}", response_model=SavedPromptOut)
def update_saved_prompt(prompt_id: int, payload: SavedPromptUpdateIn, db: Session = Depends(get_db)):
    item = db.query(SavedPrompt).filter_by(id=prompt_id, owner_key=payload.owner_key).first()
    if not item:
        raise HTTPException(status_code=404, detail="Saved prompt not found")
    db.add(SavedPromptVersion(prompt_id=item.id, title=item.title, prompt=item.prompt))
    item.title = payload.title.strip()
    item.prompt = payload.prompt
    db.commit()
    db.refresh(item)
    return item


@router.get("/saved-prompts/{prompt_id}/versions", response_model=list[SavedPromptVersionOut])
def get_saved_prompt_versions(prompt_id: int, owner_key: str = Query(default="local-demo", min_length=1, max_length=120), db: Session = Depends(get_db)):
    item = db.query(SavedPrompt).filter_by(id=prompt_id, owner_key=owner_key).first()
    if not item:
        raise HTTPException(status_code=404, detail="Saved prompt not found")
    return db.query(SavedPromptVersion).filter_by(prompt_id=prompt_id).order_by(SavedPromptVersion.created_at.desc()).all()


@router.delete("/saved-prompts/{prompt_id}")
def delete_saved_prompt(prompt_id: int, owner_key: str = Query(default="local-demo"), db: Session = Depends(get_db)):
    item = db.query(SavedPrompt).filter_by(id=prompt_id, owner_key=owner_key).first()
    if not item:
        raise HTTPException(status_code=404, detail="Saved prompt not found")
    db.delete(item)
    db.commit()
    return {"deleted": True, "id": prompt_id}


@router.get("/ai/status")
async def ai_status():
    """Report configured provider availability without exposing credentials."""
    import httpx
    ollama_available = False
    try:
        async with httpx.AsyncClient(timeout=2.5) as client:
            response = await client.get(settings.ollama_base_url.rstrip("/") + "/api/tags")
            ollama_available = response.status_code == 200
    except Exception:
        pass
    return {
        "providers": [
            {"id": "ollama", "configured": True, "available": ollama_available, "default_model": settings.ollama_model, "local": True},
            {"id": "openai", "configured": bool(settings.openai_api_key), "available": bool(settings.openai_api_key), "default_model": settings.openai_model, "local": False},
        ]
    }

@router.post("/execute/{provider}")
async def execute_provider(provider: str, payload: ExecuteIn):
    """Execute a user-supplied prompt using an explicitly configured provider."""
    if provider == "ollama":
        adapter = OllamaAdapter()
    elif provider == "openai":
        adapter = OpenAIAdapter()
    else:
        raise HTTPException(status_code=404, detail="Unsupported provider. Choose ollama or openai.")
    try:
        return await adapter.generate(payload.prompt, payload.model)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Provider request failed: {type(exc).__name__}")
