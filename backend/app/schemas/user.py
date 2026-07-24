from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "annotator"


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    role: str
    trust_score: float
    is_banned: bool
    created_at: datetime


class UserAdminUpdate(BaseModel):
    role: str | None = None
    is_banned: bool | None = None
    trust_score: float | None = None


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead
