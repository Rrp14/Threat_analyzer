from contextlib import asynccontextmanager
from app.api.endpoints.health import router as health_router
from app.api.endpoints.analyze import router as analyze_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.core.logger import configure_logging,get_logger
from app.database.db import init_db
from app.core.exceptions import DatabaseError 
from app.api.endpoints.analyses import (
    router as analyses_router
)
from app.api.endpoints.detection_generation import (
    router as detection_generation_router
)
from app.api.endpoints.report_generation import router as report_generator_router
from app.api.endpoints.intelligence import router as intelligent_router
from app.api.endpoints.graph_generation import (
    router as graph_router,
)
from app.api.endpoints.attack_path_generation import (
    router as attack_path_router,
)
from app.api.endpoints.search import router as search_router



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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(analyze_router)
app.include_router(analyses_router)
app.include_router(report_generator_router)
app.include_router(
    detection_generation_router
)
app.include_router(intelligent_router)
app.include_router(
    graph_router
)
app.include_router(
    attack_path_router
)
app.include_router(search_router)



