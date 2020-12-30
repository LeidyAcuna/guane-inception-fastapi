from uuid import uuid4
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from .base import Base

class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True, index=True)

    dogs = relationship("Dog", cascade="all,delete")