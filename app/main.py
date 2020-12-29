import logging
from fastapi import FastAPI

from app.api.api import api_router
from app.infra.postgres.models import base

log = logging.getLogger(__name__)


# Create all tables in database.
base.Base.metadata.create_all(bind=base.engine)


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")


app.include_router(api_router, prefix="/api")