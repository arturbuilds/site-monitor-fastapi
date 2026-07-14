from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    
    model_config={"from_attributes": True}

class SiteCreate(BaseModel):
    name: str
    url: str

class SiteResponse(BaseModel):
    id: int
    url: str
    name: str
    status_code: Optional[int]
    is_online: bool
    last_checked: Optional[datetime]
    user_id: int

    model_config={"from_attributes": True}