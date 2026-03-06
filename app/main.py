from contextlib import asynccontextmanager

from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.core.telemetry import configure_telemetry
from app.db.session import close_db_engine

settings = get_settings()
configure_logging()
tracer_provider = configure_telemetry(settings)


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    await close_db_engine()
    if tracer_provider is not None:
        tracer_provider.shutdown()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs" if settings.docs_enabled else None,
    redoc_url="/redoc" if settings.docs_enabled else None,
    openapi_url="/openapi.json" if settings.docs_enabled else None,
    lifespan=lifespan,
)

app.include_router(api_router, prefix=settings.api_prefix)
Instrumentator().instrument(app).expose(app, include_in_schema=False, endpoint="/metrics")
if settings.otel_enabled:
    FastAPIInstrumentor.instrument_app(app)
