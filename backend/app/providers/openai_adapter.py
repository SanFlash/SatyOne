import time
from app.core.config import settings

class OpenAIAdapter:
    slug = "openai"
    async def generate(self, prompt: str, model: str | None = None) -> dict:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured on the server.")
        from openai import AsyncOpenAI
        selected_model = model or settings.openai_model
        started = time.perf_counter()
        client = AsyncOpenAI(api_key=settings.openai_api_key, timeout=settings.provider_timeout_seconds)
        response = await client.responses.create(model=selected_model, input=prompt)
        output = response.output_text
        if not output:
            raise RuntimeError("OpenAI returned an empty response.")
        return {"provider": self.slug, "model": selected_model, "output": output, "duration_ms": round((time.perf_counter()-started)*1000)}
