# SatyOne

**One Intelligence. Every AI. Unlimited Possibilities.**

SatyOne is a local-first AI command intelligence workspace. It includes a searchable command catalogue, prompt builder, saved prompts, provider directory and repeatable workflow playbooks.

## Local-first architecture

- **Frontend:** React + TypeScript + Vite
- **Backend:** FastAPI + SQLAlchemy
- **Database:** SQLite — created automatically at `backend/data/satyone.db`
- **AI execution:** optional server-side OpenAI adapter; prompt building and catalogue features work without an API key

No Supabase, PostgreSQL, Docker or paid database is required to run the local application.

## Run on Windows

1. Install Python 3.11+ and Node.js 20+.
2. Clone this repository.
3. Double-click `start-local.bat`.

The script creates a virtual environment, installs dependencies, initializes the SQLite database and starts the API and frontend in separate terminal windows.

Open:
- App: http://localhost:5173
- API health: http://127.0.0.1:8000/health
- API documentation: http://127.0.0.1:8000/docs

### Manual setup

Backend terminal:
```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python -m app.init_db
uvicorn app.main:app --reload
```

Frontend terminal:
```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

## Local database

The database file is created at:

```text
backend/data/satyone.db
```

Tables are created automatically and the starter command/provider/workflow catalogue is seeded idempotently. User-created saved prompts are stored in this SQLite file.

To back up the database, stop the API and copy `backend/data/satyone.db` to a safe location. Do not commit the database file or environment secrets.

To rebuild the starter database from scratch, stop the API, back up the database, delete `backend/data/satyone.db`, and run `python -m app.init_db` from the `backend` directory. This deletes locally saved prompts too.

## Vercel deployment — important limitation

Vercel can host the React frontend, but its serverless filesystem is ephemeral. A SQLite file written by a Vercel function is not a durable shared database and can disappear between invocations or instances. Therefore this repository's local SQLite mode is intended for a local desktop/development server, not as a persistent database behind a public Vercel deployment.

The current Vercel deployment is a frontend deployment only. To make a public multi-user deployment persistent, the backend must run on a host with a persistent disk (or use a managed database). Do not point a public Vercel frontend at `localhost`; localhost means the visitor's own computer.

## Optional AI execution

Set `OPENAI_API_KEY` and `OPENAI_MODEL` in `backend/.env`. The key is read by the backend only and must never be placed in a `VITE_*` frontend variable. Without a key, the local command catalogue and prompt builder remain usable.

## Checks

Backend:
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest -q
```

Frontend:
```powershell
cd frontend
npm install
npm run build
```

GitHub Actions runs backend tests and the frontend production build on pushes and pull requests to `main`.

## Current scope and security notes

- Slash patterns such as `/DEEPDIVE` are SatyOne prompt macros, not universal commands understood natively by every AI provider.
- Provider directory entries are references, not claims of a live integration.
- The starter app is a local single-user workspace. Do not expose its unauthenticated saved-prompt endpoints to the public internet.
- Before enabling public accounts, add authentication, authorization, request limits, database migrations, backups and privacy controls.
