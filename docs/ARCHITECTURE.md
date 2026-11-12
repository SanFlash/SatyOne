# SatyOne architecture

Browser -> React/Vite -> FastAPI -> SQLAlchemy -> SQLite locally or managed PostgreSQL in production.

The frontend is a Vercel static deployment. The Python API is a separate Render web service defined in `render.yaml`.

Trust boundaries:
- Browser content and imported/community prompts are untrusted.
- Provider credentials remain server-side.
- Model responses are untrusted and should be rendered safely.
- Provider compatibility must be evidence-based.
- Add authentication, owner-scoped authorization, rate limiting, migrations and backups before production use.
