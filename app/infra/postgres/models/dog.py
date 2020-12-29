from uuid import uuid4
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from .base import Base


class Dog(Base):
    __tablename__ = "dog"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String)
    picture = Column(String)
    create_date = Column(String)
    is_adopted = Column(Boolean)