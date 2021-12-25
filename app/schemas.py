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


class EmployeeTypeCreate(BaseModel):
    role_name: str

    class Config:
        orm_mode = True


class EmployeeType(EmployeeTypeCreate):
    employee_type_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class EmployeeOut(BaseModel):
    employee_id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class EmployeeCreate(BaseModel):
    employee_name: str
    # Creating a default user called the normal user.
    employee_type_id: int = 4
    email: EmailStr
    password: str


class EmployeeLogin(BaseModel):
    email: EmailStr
    password: str


class Employee(BaseModel):
    employee_id: int
    email: EmailStr
    employee_name: str
    employee_type: EmployeeTypeCreate
    created_at: datetime

    class Config:
        orm_mode = True


class EmployeeShort(BaseModel):
    employee_id: int
    employee_name: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    employee_id: Optional[str] = None

# ----------------------------------------------


class SimpleEmployee(BaseModel):
    employee_id: int
    employee_name: str
    employee_type: EmployeeTypeCreate

    class Config:
        orm_mode = True


class InitiativeTypeCreate(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True


class InitiativeTypeSimple(BaseModel):
    name: str

    class Config:
        orm_mode = True


class InitiativeType(InitiativeTypeCreate):
    initiative_type_id: int

    class Config:
        orm_mode = True


class InitiativeTypeUpdate(InitiativeType):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class InitiativeTypeComplete(InitiativeTypeUpdate):
    creator: SimpleEmployee
    updater: SimpleEmployee

    class Config:
        orm_mode = True

# ----------------------------------------------


class StatusCodeCreate(BaseModel):
    description: str

    class Config:
        orm_mode = True


class StatusCode(StatusCodeCreate):
    status_id: int

    class Config:
        orm_mode = True


class StatusCodeUpdate(StatusCode):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class StatusCodeComplete(StatusCodeUpdate):
    creator: SimpleEmployee
    updater: SimpleEmployee

    class Config:
        orm_mode = True

# ----------------------------------------------


class InitiativeCreate(BaseModel):
    title: str
    description: str
    # setting the default to: meetups
    initiative_type: int = 2
    # setting the default to: In Discussion
    status_id: int = 3

    class Config:
        orm_mode = True


class Initiative(InitiativeCreate):
    initiative_id: int
    init_type: InitiativeType

    class Config:
        orm_mode = True


class InitiativeSimple(BaseModel):
    initiative_id: int
    title: str
    description: str
    init_type: InitiativeTypeSimple
    status: StatusCodeCreate

    class Config:
        orm_mode = True


class InitiativeShort(BaseModel):
    initiative_id: int
    title: str

    class Config:
        orm_mode = True


class InitiativeUpdate(Initiative):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class InitiativeComplete(InitiativeUpdate):
    status: StatusCodeCreate
    creator: SimpleEmployee
    updater: SimpleEmployee

    class Config:
        orm_mode = True

# ----------------------------------------------


class TaskLogCreate(BaseModel):
    initiative_id: int
    description: str

    class Config:
        orm_mode = True


class TaskLog(TaskLogCreate):
    task_id: int
    initiative: InitiativeSimple

    class Config:
        orm_mode = True


class TaskLogSimple(BaseModel):
    task_id: int
    description: str
    initiative: InitiativeShort
    creator: EmployeeShort

    class Config:
        orm_mode = True


class TaskLogUpdate(TaskLogSimple):
    logged_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TaskLogComplete(TaskLogUpdate):
    creator: SimpleEmployee

    class Config:
        orm_mode = True

# ----------------------------------------------


class ReviewCreate(BaseModel):
    initiative_id: int
    description: str

    class Config:
        orm_mode = True


class Review(ReviewCreate):
    review_id: int
    initiative: InitiativeSimple

    class Config:
        orm_mode = True


class ReviewSimple(BaseModel):
    review_id: int
    description: str
    initiative: InitiativeShort
    reviewer: EmployeeShort

    class Config:
        orm_mode = True


class ReviewUpdate(ReviewSimple):
    given_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ReviewComplete(ReviewUpdate):
    reviewer: SimpleEmployee

    class Config:
        orm_mode = True

# ----------------------------------------------


class RatingCreate(BaseModel):
    initiative_id: int
    point: int

    class Config:
        orm_mode = True


class Rating(RatingCreate):
    rating_id: int
    initiative: InitiativeSimple

    class Config:
        orm_mode = True


class RatingSimple(BaseModel):
    rating_id: int
    point: int
    initiative: InitiativeShort
    rater: EmployeeShort

    class Config:
        orm_mode = True


class RatingUpdate(RatingSimple):
    given_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class RatingComplete(RatingUpdate):
    rater: SimpleEmployee

    class Config:
        orm_mode = True
