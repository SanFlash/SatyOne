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

## Cross-industry role library

SatyOne is designed as a cross-industry prompt and workflow workspace, not a QA-only command tool. Its command catalogue includes software and QA, business strategy, project management, finance and accounting, marketing and sales, HR and recruiting, education, healthcare administration and clinician-reviewed patient education, legal operations and compliance drafting, science and research, engineering and manufacturing, design and media, hospitality and travel, public sector and nonprofit work, real estate and construction, customer support, supply chain and logistics, and personal productivity.

Each role template is intended to provide a useful starting point with a purpose, detailed instruction, example input, expected output, tags and professional limitations. The catalogue is extensible: add new role categories and command templates as real user needs emerge. No finite catalogue can enumerate every occupation or jurisdiction. For regulated or safety-critical work, prompts are organizational aids only and do not replace qualified professional judgment, applicable standards, or legal review.

## Advanced productivity modules

- **Command Studio:** create reusable slash macros with a role category, detailed instruction template, example input and a quality checklist. Custom commands are stored in browser local storage on that browser; they are not synchronized between devices or users.
- **Command variants:** choose concise, beginner, professional, expert, strict, creative or audit-style output in the prompt builder. A variant changes the instruction requirements; it does not change the underlying model or grant new capabilities.
- **Knowledge Studio:** paste source text or import a text-based TXT, Markdown, CSV, JSON or LOG file (up to 1 MB). The extracted text is placed into the prompt context locally. This is not a document search index, OCR engine, PDF parser or cloud upload service. Review imported content and remove secrets before use.
- **Expanded catalogue:** the connected and offline experiences merge the bundled cross-industry catalogue, so the broader local command collection remains searchable even when the backend catalogue is older or unavailable.
- **Free tools directory:** search references to local AI runtimes, development tools, testing, data, design and security utilities. Each tool must be installed/configured separately. Directory entries do not mean SatyOne can launch or control those tools.

### Local model workspace setup

For a private, local-model workflow, install [Ollama](https://ollama.com/) on the same computer as the FastAPI backend, download a model that fits your hardware and configure `OLLAMA_BASE_URL` and `OLLAMA_MODEL` in `backend/.env`. SatyOne's backend now has an Ollama adapter and the Prompt Builder can send prompts to it. Never expose an unauthenticated local model endpoint to the public internet.

## Free and open-source tool directory

The directory contains references to local-first and open-source tools across AI/model serving, coding, API development, browser testing, data analysis, design, office productivity, observability, databases and authorized defensive security. Examples include Ollama, llama.cpp, Open WebUI, LibreChat, Dify, Flowise, Langflow, Playwright, Selenium, pytest, Bruno, Jupyter, DuckDB, PostgreSQL, Penpot, GIMP, Inkscape, Blender, LibreOffice, Prometheus, Wireshark and OWASP ZAP.

**Pricing and licensing are not interchangeable.** The directory labels open-source/self-hosted software separately from hosted free plans, freemium services and source-available projects. Free tiers, licenses, eligibility, quotas and commercial-use conditions can change; verify the official project page before adoption. Self-hosted software may still require hardware, storage, administration and paid model/API access. Directory inclusion does not mean SatyOne has integrated or security-tested that product.

## Command variants and professional workflows

The command catalogue is an extensible set of prompt macros, not a universal executable shell. Each macro should state its purpose, detailed instruction, example input, expected output, tags, difficulty and limitations. Variants cover planning, analysis, execution preparation, review, quality control, reporting, risk and communication across professional domains. Users should adapt placeholders and validate high-impact output with accountable experts.

## Browser-only offline workspace

The frontend now includes a bundled local command catalogue and an offline prompt builder. If the API is unreachable (including on a frontend-only Vercel deployment), Command Explorer, search/filtering and prompt generation continue to work without starting FastAPI.

Saved prompts created in this mode are stored in the current browser's local storage. They are not synchronized across browsers or devices and can be cleared when site data is removed. When the FastAPI backend is available, the app uses the backend SQLite database instead. The browser-only mode does not execute AI model requests; it creates reusable prompt instructions.

The Vercel rewrite currently serves the static React application and does not host the FastAPI backend. For server-backed prompt history, shared data and AI execution, deploy the FastAPI backend separately and configure `VITE_API_BASE_URL` to its HTTPS API base URL. Use a persistent managed database for public hosting; do not use ephemeral serverless SQLite for durable user data.

## Vercel deployment — important limitation

Vercel can host the React frontend, but its serverless filesystem is ephemeral. A SQLite file written by a Vercel function is not a durable shared database and can disappear between invocations or instances. Therefore this repository's local SQLite mode is intended for a local desktop/development server, not as a persistent database behind a public Vercel deployment.

The current Vercel deployment is a frontend deployment only. To make a public multi-user deployment persistent, the backend must run on a host with a persistent disk (or use a managed database). Do not point a public Vercel frontend at `localhost`; localhost means the visitor's own computer.

## Live AI execution

The Prompt Builder includes an execution panel for **Ollama (local)** and **OpenAI (hosted API)**. Requests are sent from the browser to FastAPI; provider credentials and local endpoint configuration stay on the backend.

### Ollama — local and private

1. Install Ollama from [ollama.com](https://ollama.com/) on the same machine running FastAPI.
2. In a terminal, run `ollama pull llama3.2` (or download another model supported by your hardware).
3. Set `OLLAMA_BASE_URL=http://127.0.0.1:11434` and `OLLAMA_MODEL=llama3.2` in `backend/.env`.
4. Restart FastAPI, open SatyOne Prompt Builder, generate a prompt, select Ollama and click **Run with selected AI provider**.

Check `GET /api/v1/ai/status` or `http://127.0.0.1:8000/docs` to inspect configured provider availability. Model downloads can be several GB; hardware requirements vary. Keep Ollama bound to localhost and do not expose its unauthenticated API publicly.

### OpenAI — hosted API

Set `OPENAI_API_KEY` and `OPENAI_MODEL` in `backend/.env`, restart FastAPI, select OpenAI in the builder and execute. API usage may incur charges. The key is read by the backend only and must never be placed in a `VITE_*` frontend variable.

`PROVIDER_TIMEOUT_SECONDS` controls the server-side request timeout (default 120). Only the explicit `ollama` and `openai` provider IDs are accepted. The backend returns the model output and execution duration; it does not execute arbitrary tools or external actions.

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
- The starter app is a local single-user workspace. Do not expose its unauthenticated saved-prompt or AI execution endpoints to the public internet. Provider execution has no per-user quotas or billing controls in this release.
- Before enabling public accounts, add authentication, authorization, request limits, database migrations, backups and privacy controls.

## Product scope, legal and security governance

SatyOne is being expanded as a modular AI command-intelligence platform. Its intended knowledge domains include AI fundamentals, prompt engineering, provider/model comparison, software engineering, QA and automation, data analysis, research, creative workflows, defensive security, privacy, integrations and bounded agent workflows.

The product deliberately distinguishes educational content and prompt templates from verified integrations and production-supported capabilities. It does not promise universal provider compatibility or guarantee generated output.

Read the governance specifications:
- [Product scope, capability map and boundaries](docs/PRODUCT_SCOPE_AND_CAPABILITIES.md)
- [Legal and responsible-use policy](docs/LEGAL_AND_RESPONSIBLE_USE.md)
- [Security, privacy and AI governance baseline](docs/SECURITY_PRIVACY_GOVERNANCE.md)
- [Product roadmap and release gates](docs/ROADMAP.md)

These documents are engineering and policy baselines, not legal advice or a certification of compliance. Before public launch, obtain qualified legal review for the operator's jurisdictions, data flows, provider contracts and actual feature set. India-facing operations must assess the phased commencement of the DPDP Act and Rules and applicable CERT-In directions.

## Current release boundary

The current codebase remains a local-first single-user starter. The documentation describes the intended product scope and release gates; it does not mean every listed capability has already been implemented. Public multi-user launch requires authentication, object-level authorization, tenant isolation, abuse controls, privacy workflows, persistent hosting, tested backups and security/legal review.
