from sqlalchemy import Column, String, Uuid, Boolean, DateTime
from src.configs.database import Base
from pydantic import BaseModel, Field

class Users(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, nullable=False)
    email = Column(String)
    fullname = Column(String)
    password = Column(String)
    status = Column(String, comment="S1 = active, S2 = not active")
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=None)
    created_by = Column(Uuid, default=None)
    updated_at = Column(DateTime, default=None)
    updated_by = Column(Uuid, default=None)

class Payload(BaseModel):
    email: str | None = Field(title="Email cannot be empty", max_length=50, min_length=5)
    password: str | None = Field(default=None, min_length=8)
    fullname: str | None = Field(title="Fullname cannot be empty", min_length=1)
    status: str | None = Field(title="Status cannot be empty", min_length=2, max_length=2)

class PayloadInsert(Payload):
    password: str | None = Field(title="Password cannot be empty", min_length=8)