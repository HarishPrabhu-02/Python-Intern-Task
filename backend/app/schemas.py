from pydantic import BaseModel
from typing import Optional

# ==========================
# User Schemas
# ==========================
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    
    # This tells Pydantic to read data even if it's an SQLAlchemy model, not just a dict
    class Config:
        from_attributes = True

# ==========================
# Task Schemas
# ==========================
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(TaskBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

# ==========================
# Authentication Schemas
# ==========================
class Token(BaseModel):
    access_token: str
    token_type: str