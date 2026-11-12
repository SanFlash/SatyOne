from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class CategoryOut(BaseModel):
    id:int; slug:str; name:str; description:str; icon:str
    model_config=ConfigDict(from_attributes=True)

class CommandOut(BaseModel):
    id:int; slug:str; name:str; syntax:str; description:str; instruction_template:str
    example_input:str; example_output:str; difficulty:str; status:str; tags:list[str]
    limitations:str; category:CategoryOut
    model_config=ConfigDict(from_attributes=True)

class PromptBuildIn(BaseModel):
    objective:str=Field(min_length=5,max_length=5000)
    audience:str="general"
    tone:str="clear and professional"
    output_format:str="structured response"
    constraints:list[str]=Field(default_factory=list)
    command_slugs:list[str]=Field(default_factory=list)

class PromptBuildOut(BaseModel):
    prompt:str
    selected_commands:list[str]
    notes:list[str]

class SavedPromptIn(BaseModel):
    title:str=Field(min_length=1,max_length=180)
    prompt:str=Field(min_length=1,max_length=20000)
    owner_key:str=Field(default="local-demo", min_length=1, max_length=120)

class SavedPromptOut(BaseModel):
    id:int; title:str; prompt:str; owner_key:str
    model_config=ConfigDict(from_attributes=True)


class SavedPromptUpdateIn(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    prompt: str = Field(min_length=1, max_length=20000)
    owner_key: str = Field(default="local-demo", min_length=1, max_length=120)

class SavedPromptVersionOut(BaseModel):
    id: int
    prompt_id: int
    title: str
    prompt: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ExecuteIn(BaseModel):
    prompt: str = Field(min_length=1, max_length=30000)
    model: str | None = Field(default=None, max_length=160)

class ExecuteOut(BaseModel):
    provider: str
    model: str
    output: str
    duration_ms: int
