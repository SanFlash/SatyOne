from app.core.config import settings

class OpenAIAdapter:
    slug="openai"
    async def generate(self,prompt:str,model:str|None=None)->dict:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured on the server.")
        from openai import AsyncOpenAI
        client=AsyncOpenAI(api_key=settings.openai_api_key)
        selected_model=model or settings.openai_model
        response=await client.responses.create(model=selected_model,input=prompt)
        return {"provider":self.slug,"model":selected_model,"output":response.output_text}
