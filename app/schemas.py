"""
    We use pydantic models that does the part of data
    validation.

    It is because of this we can ensure that whatever
    data is sent by the frontend is in compliance
    with the backend.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class EmployeeTypeCreate(BaseModel):
    role_name: str


class EmployeeType(EmployeeTypeCreate):
    employee_type_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class EmployeeOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class EmployeeCreate(BaseModel):
    employee_name: str
    employee_type_id: int
    email: EmailStr
    password: str


class EmployeeLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
