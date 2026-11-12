import time
import httpx
from app.core.config import settings

class OllamaAdapter:
    slug = "ollama"

    async def generate(self, prompt: str, model: str | None = None) -> dict:
        selected_model = model or settings.ollama_model
        base = settings.ollama_base_url.rstrip("/")
        started = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=settings.provider_timeout_seconds) as client:
                response = await client.post(f"{base}/api/generate", json={"model": selected_model, "prompt": prompt, "stream": False})
                response.raise_for_status()
                data = response.json()
        except httpx.ConnectError as exc:
            raise RuntimeError("Cannot reach Ollama. Start Ollama locally and verify OLLAMA_BASE_URL.") from exc
        except httpx.TimeoutException as exc:
            raise RuntimeError("Ollama request timed out. Try a smaller model or increase PROVIDER_TIMEOUT_SECONDS.") from exc
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(f"Ollama returned HTTP {exc.response.status_code}: {exc.response.text[:500]}") from exc
        output = data.get("response")
        if not isinstance(output, str) or not output.strip():
            raise RuntimeError("Ollama returned an empty response. Check that the selected model is installed.")
        return {"provider": self.slug, "model": selected_model, "output": output, "duration_ms": round((time.perf_counter()-started)*1000)}
