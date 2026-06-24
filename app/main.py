from contextlib import asynccontextmanager
from app.api.endpoints.health import router as health_router
from app.api.endpoints.ingest import router as ingest_router
from app.api.endpoints.extract import router as extract_router
from app.api.endpoints.enrich import router as enrich_router
from fastapi import FastAPI
from app.config import settings
from app.core.logger import configure_logging,get_logger
from app.database.db import init_db
from app.core.exceptions import DatabaseError 


logger=get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    configure_logging()
    logger.info("Application starting...")

  
    try:
        logger.info("Initializing database...")
        init_db()
        logger.info("Database successfully initialized.")
        
    except Exception as exc:
        custom_error = DatabaseError(
            message=f"Critical failure during database startup initialization: {str(exc)}",
            details={"original_exception": exc.__class__.__name__}
        )
        
        logger.exception(
            "Application startup failed", 
            error_data=custom_error.to_dict()
        )
        
        raise custom_error

    yield 

   
    logger.info("Application shutting down...")


app=FastAPI(
        title="Threat Intelligence Platform",
        description="AI-Powered Threat Intelligence Backend",
        version=settings.app_version,

        lifespan=lifespan
    )

app.include_router(health_router)
app.include_router(ingest_router)
app.include_router(extract_router)
app.include_router(enrich_router)


