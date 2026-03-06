# Production FastAPI Template

Production-ready FastAPI starter focused on team distribution and real deployment needs:
- PostgreSQL with SQLAlchemy 2.0 async
- Alembic migrations
- Structured logging
- Prometheus metrics
- Optional OpenTelemetry tracing
- Docker + docker-compose
- CI with GitHub Actions
- Linting, formatting, typing, tests, and security checks

## 1. Why this template

This template is designed to be a baseline your team can clone for new services without re-solving platform concerns. It ships with:
- Clean app architecture (`api`, `services`, `repositories`, `db`, `core`)
- Versioned APIs (`/api/v1`)
- Health checks for K8s/load balancers
- Observability endpoints and hooks
- Reproducible local and CI workflows

## 2. Project structure

```text
.
|-- app/
|   |-- main.py
|   |-- api/
|   |   `-- v1/endpoints/
|   |-- core/
|   |-- db/
|   |-- models/
|   |-- repositories/
|   |-- schemas/
|   `-- services/
|-- alembic/
|   `-- versions/
|-- infra/
|   `-- monitoring/prometheus.yml
|-- tests/
|-- .github/workflows/ci.yml
|-- docker-compose.yml
|-- Dockerfile
`-- pyproject.toml
```

## 3. What is included (and why)

1. API framework: [FastAPI](https://fastapi.tiangolo.com/)
Purpose: high-performance async API framework with automatic OpenAPI docs.

2. ASGI server: [Uvicorn](https://www.uvicorn.org/)
Purpose: production-capable ASGI runtime.

3. Database: [PostgreSQL](https://www.postgresql.org/) + [SQLAlchemy 2.0 async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
Purpose: relational consistency, robust transactions, and scalable query layer.

4. Migrations: [Alembic](https://alembic.sqlalchemy.org/)
Purpose: deterministic schema versioning for team environments.

5. Metrics: [Prometheus](https://prometheus.io/) + [Instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator)
Purpose: scrape-ready request metrics at `/metrics`.

6. Tracing: [OpenTelemetry](https://opentelemetry.io/docs/languages/python/)
Purpose: distributed traces export via OTLP (optional, env-controlled).

7. Dashboards: [Grafana](https://grafana.com/)
Purpose: visualize Prometheus metrics quickly in local/staging setups.

8. Quality: [Ruff](https://docs.astral.sh/ruff/), [MyPy](https://mypy-lang.org/), [Pytest](https://docs.pytest.org/), [Bandit](https://bandit.readthedocs.io/)
Purpose: style, static analysis, tests, and security checks as gates.

9. Automation: [GitHub Actions](https://docs.github.com/en/actions)
Purpose: enforce quality and build reproducibility on every PR/push.

10. Dev hooks: [pre-commit](https://pre-commit.com/)
Purpose: run checks before code reaches CI.

## 4. Quick start

1. Create env file:
```powershell
Copy-Item .env.example .env
```

2. Install dependencies:
```powershell
python -m pip install --upgrade pip
pip install .[dev]
```

3. Apply migrations:
```powershell
alembic upgrade head
```

4. Run local API:
```powershell
# Using uv (recommended for reproducible environments)
uv run uvicorn app.main:app --reload

# Or plain Python if uv isn't installed
python -m uvicorn app.main:app --reload
```

5. API docs:
- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`
## 5. Docker local stack

Includes:
- `api` (FastAPI service)
- `db` (PostgreSQL 16)
- `prometheus` (metrics scraper)
- `grafana` (dashboard UI)

Run:
```powershell
Copy-Item .env.example .env
docker compose up --build
```

Endpoints:
- API: `http://localhost:8000`
- Metrics: `http://localhost:8000/metrics`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000` (admin/admin)

## 6. Database migrations

1. Apply migrations:
```powershell
alembic upgrade head
```

2. Create a migration after model changes:
```powershell
alembic revision --autogenerate -m "describe change"
```

## 7. API health and readiness

- Liveness: `GET /api/v1/health/live`
- Readiness: `GET /api/v1/health/ready`

`ready` performs a DB check, suitable for load balancer and orchestration probes.

## 8. Observability model

1. Logs:
- JSON structured logs by default (`LOG_JSON=true`)
- Log level via `LOG_LEVEL`

2. Metrics:
- Prometheus at `/metrics`
- Request counters and latency histograms

3. Traces:
- Enable with `OTEL_ENABLED=true`
- Export to `OTEL_EXPORTER_OTLP_ENDPOINT`

## 9. CI/CD baseline

Workflow file: `.github/workflows/ci.yml`

Checks:
- Ruff lint
- Ruff format check
- MyPy type check
- Pytest + coverage threshold
- Bandit security scan
- Docker image build

Recommended extensions for your org:
- Push image to GHCR/ECR/GCR
- Deploy to staging on merge
- Add integration tests against ephemeral environment
- Add SAST/Dependency scanners (CodeQL, Trivy, pip-audit)

## 10. Environment variables

Important variables in `.env.example`:
- `DATABASE_URL`: Async SQLAlchemy PostgreSQL DSN
- `ENVIRONMENT`: `development`/`staging`/`production`
- `DOCS_ENABLED`: disable docs in production if required
- `OTEL_*`: tracing controls

## 11. Production hardening checklist

1. Add auth and authorization (`OAuth2/JWT`, RBAC/ABAC).
2. Add rate limiting and abuse protections.
3. Set strict CORS policy and trusted host middleware.
4. Add secrets management (Vault/AWS Secrets Manager/GCP Secret Manager).
5. Add backup policy and migration rollback process.
6. Configure SLA-based alerts from Prometheus/Grafana.
7. Add blue-green or canary deployment strategy.
8. Use non-root Docker user and image signing.

## 12. Suggested next template modules

1. Redis caching + task queue (`RQ` or `Celery`).
2. Auth module (users, sessions, permissions).
3. API key management and tenant isolation.
4. Outbox/event publishing pattern for microservices.
5. Contract tests for external integrations.






# fastapi-prod-template
