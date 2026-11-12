from sqlalchemy.orm import Session
from app.models import Command
from app.schemas import PromptBuildIn

def build_prompt(payload:PromptBuildIn,db:Session):
    commands=db.query(Command).filter(Command.slug.in_(payload.command_slugs)).all() if payload.command_slugs else []
    sections=[
        "You are an AI assistant helping complete the user's stated objective.",
        f"OBJECTIVE:\n{payload.objective.strip()}",
        f"AUDIENCE: {payload.audience}",
        f"TONE: {payload.tone}",
        f"OUTPUT FORMAT: {payload.output_format}",
    ]
    notes=[]
    for command in commands:
        sections.append(f"INSTRUCTION PATTERN — {command.name} ({command.syntax}):\n{command.instruction_template}")
        notes.append(f"{command.syntax} is a SatyOne macro pattern; adapt placeholders and verify model compatibility.")
    if payload.constraints:
        sections.append("CONSTRAINTS:\n"+"\n".join(f"- {item}" for item in payload.constraints))
    sections.append("QUALITY CHECK: State assumptions, identify missing information, and do not invent facts, sources, tool access or completed actions.")
    return {"prompt":"\n\n".join(sections),"selected_commands":[c.syntax for c in commands],"notes":notes}
