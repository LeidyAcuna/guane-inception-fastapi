from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker

from app.infra.postgres.crud.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@as_declarative()
class Base:
    id: Any
    
    
