@echo off
setlocal

set HOST=0.0.0.0
set PORT=8000
set WORKERS=5

echo Applying database migrations...
alembic upgrade head
if errorlevel 1 (
  echo Migration failed. Fix database connection or migration issues, then retry.
  exit /b 1
)

echo Starting FastAPI (load test mode)...
uvicorn app.main:app --host %HOST% --port %PORT% --workers %WORKERS% --no-access-log