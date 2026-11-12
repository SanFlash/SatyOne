from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session,joinedload
from app.db import get_db
from app.models import Category,Command,Provider,Workflow,SavedPrompt
from app.schemas import PromptBuildIn,PromptBuildOut,SavedPromptIn,SavedPromptOut
from app.services.prompt_builder import build_prompt
from app.providers.openai_adapter import OpenAIAdapter
router=APIRouter()

@router.get("/categories")
def list_categories(db:Session=Depends(get_db)):
    return db.query(Category).order_by(Category.name).all()

@router.get("/commands")
def list_commands(q:str|None=None,category:str|None=None,difficulty:str|None=None,db:Session=Depends(get_db)):
    query=db.query(Command).options(joinedload(Command.category))
    if q:
        term=f"%{q.strip()}%"
        query=query.filter((Command.name.ilike(term))|(Command.syntax.ilike(term))|(Command.description.ilike(term))|(Command.instruction_template.ilike(term)))
    if category:query=query.join(Category).filter(Category.slug==category)
    if difficulty:query=query.filter(Command.difficulty==difficulty)
    return query.order_by(Command.name).all()

@router.get("/commands/{slug}")
def get_command(slug:str,db:Session=Depends(get_db)):
    item=db.query(Command).options(joinedload(Command.category)).filter_by(slug=slug).first()
    if not item:raise HTTPException(404,"Command not found")
    return item

@router.post("/commands/seed")
def reseed_commands(db:Session=Depends(get_db)):
    from app.seed import seed_catalog
    seed_catalog(db)
    return {"message":"Starter catalogue ensured."}

@router.get("/providers")
def list_providers(db:Session=Depends(get_db)):
    return db.query(Provider).order_by(Provider.name).all()

@router.get("/workflows")
def list_workflows(db:Session=Depends(get_db)):
    return db.query(Workflow).order_by(Workflow.name).all()

@router.post("/prompt-builder",response_model=PromptBuildOut)
def prompt_builder(payload:PromptBuildIn,db:Session=Depends(get_db)):
    return build_prompt(payload,db)

@router.post("/saved-prompts",response_model=SavedPromptOut)
def save_prompt(payload:SavedPromptIn,db:Session=Depends(get_db)):
    item=SavedPrompt(title=payload.title,prompt=payload.prompt,owner_key=payload.owner_key)
    db.add(item);db.commit();db.refresh(item);return item

@router.get("/saved-prompts",response_model=list[SavedPromptOut])
def get_saved_prompts(owner_key:str="local-demo",db:Session=Depends(get_db)):
    return db.query(SavedPrompt).filter_by(owner_key=owner_key).order_by(SavedPrompt.created_at.desc()).all()

@router.post("/execute/openai")
async def execute_openai(payload:PromptBuildIn,db:Session=Depends(get_db)):
    built=build_prompt(payload,db)
    try:return await OpenAIAdapter().generate(built["prompt"])
    except RuntimeError as exc:raise HTTPException(400,str(exc))
    except Exception as exc:raise HTTPException(502,f"Provider request failed: {type(exc).__name__}")
