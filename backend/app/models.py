from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

def utcnow():
    return datetime.now(timezone.utc)

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text, default="")
    icon: Mapped[str] = mapped_column(String(40), default="sparkles")
    commands = relationship("Command", back_populates="category")

class Command(Base):
    __tablename__ = "commands"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(140), index=True)
    syntax: Mapped[str] = mapped_column(String(80), index=True)
    description: Mapped[str] = mapped_column(Text)
    instruction_template: Mapped[str] = mapped_column(Text)
    example_input: Mapped[str] = mapped_column(Text, default="")
    example_output: Mapped[str] = mapped_column(Text, default="")
    difficulty: Mapped[str] = mapped_column(String(30), default="beginner")
    status: Mapped[str] = mapped_column(String(30), default="reviewed")
    tags: Mapped[list] = mapped_column(JSON, default=list)
    limitations: Mapped[str] = mapped_column(Text, default="")
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    category = relationship("Category", back_populates="commands")

class Provider(Base):
    __tablename__ = "providers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True)
    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text, default="")
    docs_url: Mapped[str] = mapped_column(String(500), default="")
    integration_status: Mapped[str] = mapped_column(String(40), default="directory")

class Workflow(Base):
    __tablename__ = "workflows"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    name: Mapped[str] = mapped_column(String(160))
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(80), default="general")
    difficulty: Mapped[str] = mapped_column(String(30), default="beginner")
    steps: Mapped[list] = mapped_column(JSON, default=list)

class SavedPrompt(Base):
    __tablename__ = "saved_prompts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_key: Mapped[str] = mapped_column(String(120), index=True, default="local-demo")
    title: Mapped[str] = mapped_column(String(180))
    prompt: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class CommandProvider(Base):
    __tablename__ = "command_providers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    command_id: Mapped[int] = mapped_column(ForeignKey("commands.id"))
    provider_slug: Mapped[str] = mapped_column(String(80))
    compatibility_status: Mapped[str] = mapped_column(String(40), default="untested")
    tested_model: Mapped[str] = mapped_column(String(120), default="")
    last_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    __table_args__ = (UniqueConstraint("command_id", "provider_slug"),)
