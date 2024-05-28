from pydantic import BaseModel, Field

class Payload(BaseModel):
    email: str | None = Field(title="Email cannot be empty")
    password: str | None = Field(title="Password cannot be empty")