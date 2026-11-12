from sqlalchemy.orm import Session
from app.models import Command
from app.schemas import PromptBuildIn

def build_prompt(payload: PromptBuildIn, db: Session):
    requested = list(dict.fromkeys(payload.command_slugs))
    commands = (
        db.query(Command)
        .filter(Command.slug.in_(requested))
        .order_by(Command.name)
        .all()
        if requested else []
    )
    found = {command.slug for command in commands}
    missing = [slug for slug in requested if slug not in found]

    sections = [
        "SATYONE — STRUCTURED AI INSTRUCTION",
        "ROLE: You are an assistant helping with the user's stated objective. Be accurate, transparent and appropriately cautious.",
        f"OBJECTIVE:\n{payload.objective.strip()}",
        f"AUDIENCE: {payload.audience.strip()}",
        f"TONE: {payload.tone.strip()}",
        f"OUTPUT FORMAT: {payload.output_format.strip()}",
        "WORKING METHOD:",
        "- Clarify material ambiguity instead of silently inventing missing requirements.",
        "- Break complex work into logical, verifiable steps.",
        "- Separate confirmed facts, assumptions, estimates and recommendations.",
        "- Explain relevant trade-offs, dependencies and failure cases.",
        "- For technical work, include validation or tests and explain how to verify the result.",
        "- Do not claim to have accessed tools, files, websites, accounts or systems unless that access actually occurred.",
        "- Do not fabricate citations, test results, credentials, provider capabilities or completed actions.",
    ]

    notes = []
    for command in commands:
        sections.append(
            f"INSTRUCTION PATTERN — {command.name} ({command.syntax}):\n"
            f"{command.instruction_template}\n"
            f"LIMITATION: {command.limitations}"
        )
        notes.append(
            f"{command.syntax} is a SatyOne reusable prompt pattern, not a universal native command. "
            "Adapt placeholders and verify compatibility with the selected model."
        )

    if missing:
        notes.append("Unknown command slugs were ignored: " + ", ".join(missing))

    if payload.constraints:
        clean_constraints = [item.strip() for item in payload.constraints if item.strip()]
        if clean_constraints:
            sections.append("USER CONSTRAINTS:\n" + "\n".join(f"- {item}" for item in clean_constraints))

    sections.extend([
        "SAFETY, PRIVACY AND AUTHORIZATION:",
        "- Respect applicable law, provider terms, intellectual property, privacy and confidentiality.",
        "- Do not assist unauthorized access, credential theft, malware, destructive disruption, covert surveillance or other unlawful harm.",
        "- For security testing, require explicit authorization and a defined scope; prefer owned labs and non-destructive validation.",
        "- Minimize personal and confidential data. Recommend redaction or synthetic data when practical.",
        "- Do not perform consequential external actions without explicit user approval and appropriate permissions.",
        "FINAL QUALITY CHECK:",
        "Before responding, check that the answer addresses the objective, follows constraints, states material uncertainty and includes useful next steps or verification criteria.",
    ])

    return {
        "prompt": "\n\n".join(sections),
        "selected_commands": [command.syntax for command in commands],
        "notes": notes,
    }
