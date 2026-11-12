@echo off
setlocal
cd /d "%~dp0"
if not exist "backend\.venv\Scripts\python.exe" (
  py -3.11 -m venv backend\.venv
)
call backend\.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
if not exist "backend\.env" copy "backend\.env.example" "backend\.env"
python -m app.init_db
start "SatyOne API" cmd /k "cd /d "%~dp0backend" && ..\.venv\Scripts\activate.bat && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
cd frontend
if not exist node_modules npm install
if not exist .env copy .env.example .env
start "SatyOne Frontend" cmd /k "npm run dev"
echo.
echo SatyOne is starting.
echo Frontend: http://localhost:5173
echo API docs: http://127.0.0.1:8000/docs
echo SQLite: backend\data\satyone.db
endlocal
