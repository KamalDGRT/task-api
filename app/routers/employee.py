from typing import List
from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix='/employee',
    tags=['Employees']
)


@router.get('/all', response_model=List[schemas.Employee])
# @router.get('/')
def get_employees(
    db: Session = Depends(get_db)
):
    results = db.query(models.Employee).all()
    return results


@router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.EmployeeOut
)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db)
):
    """
    Inserting a new employee into the database
    """
    hashed_password = utils.hash(employee.password)
    employee.password = hashed_password

    new_user = models.Employee(**employee.dict())

    db_user = db.query(models.Employee).filter(
        models.Employee.email == new_user.email).first()

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Failed to create the uUser Already Exists !!!"
        )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get(
    '/info/{id}',
    response_model=schemas.Employee
)
def get_employee(
    id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(
        models.Employee
    ).filter(
        models.Employee.employee_id == id
    ).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id: {id} does not exist!"
        )
    return employee
