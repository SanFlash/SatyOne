# SatyOne

**One Intelligence. Every AI. Unlimited Possibilities.**

SatyOne is an AI command intelligence platform: searchable instruction patterns, a prompt builder, workflow catalogue and AI provider directory.

## Deployment architecture
- **Frontend:** Vercel (React/Vite static site)
- **Backend:** Render (FastAPI web service)
- **Database:** Supabase PostgreSQL or another managed PostgreSQL provider

Vercel hosts the frontend. The Python API is deployed separately using `render.yaml`; the backend is not bundled into the Vercel static frontend.

## Local setup (Windows PowerShell)

### Backend
```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```
API: http://127.0.0.1:8000  
Swagger: http://127.0.0.1:8000/docs

### Frontend (second terminal)
```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```
UI: http://localhost:5173

## Deploy frontend to Vercel
1. Import `SanFlash/SatyOne` into Vercel.
2. Keep the repository root as the project root.
3. Use the included `vercel.json` build and output settings.
4. Add `VITE_API_BASE_URL` with your deployed API URL and `/api/v1`, e.g. `https://YOUR-API.onrender.com/api/v1`.
5. Deploy. Vite environment variables are baked in at build time; redeploy after changing them.

## Deploy API to Render
1. Create a Web Service from this repository; select the included `render.yaml` blueprint.
2. Confirm root directory is `backend`.
3. Set `DATABASE_URL` to managed PostgreSQL, preferably in SQLAlchemy psycopg format: `postgresql+psycopg://USER:PASSWORD@HOST:5432/postgres`.
4. Set `FRONTEND_ORIGINS` to the exact Vercel production URL (comma-separated for preview + production URLs).
5. Add `OPENAI_API_KEY` only in Render's secret environment settings if using OpenAI execution.

## Tests
Backend: `cd backend`, activate the venv, then `pytest -q`.  
Frontend: `cd frontend`, then `npm run build`.

## Security and readiness
- Slash commands such as `/DEEPDIVE` are SatyOne-defined macros, not universal hidden AI commands.
- Provider credentials must remain server-side; never expose them through `VITE_*` variables.
- The starter saved-prompt endpoint uses a demo owner key. Implement Supabase Auth/JWT verification and owner-scoped authorization before real multi-user production use.
- Add Alembic migrations, rate limiting, backups, monitoring and privacy/legal pages before production launch.
- Provider directory presence does not imply a live or verified integration.
