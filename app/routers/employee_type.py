from fastapi import status, HTTPException, Response, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, oauth2

# Using hyphen by following this answer
# https://stackoverflow.com/a/18449772
router = APIRouter(
    prefix='/employee-type',
    tags=['Employee Type']
)


@router.get(
    '/all',
    response_model=List[schemas.EmployeeType]
)
# @router.get('/')
def get_employee_types(
    db: Session = Depends(get_db),
    current_employee: int = Depends(oauth2.get_current_employee)
):

    if current_employee.employee_type_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    results = db.query(models.EmployeeType).all()
    return results


@router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.EmployeeType,
)
def create_employee_type(
    empl_type: schemas.EmployeeTypeCreate,
    db: Session = Depends(get_db),
    current_employee: int = Depends(oauth2.get_current_employee)
):

    new_empl_type = models.EmployeeType(**empl_type.dict())
    # ** unpacks the dictionary into this format:
    # title=post.title, content=post.content, ...
    # This prevents us from specifiying individual fields

    if current_employee.employee_type_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    db.add(new_empl_type)
    db.commit()
    db.refresh(new_empl_type)

    return new_empl_type


@router.get(
    '/info/{id}',
    response_model=schemas.EmployeeType
)
def get_employee_type(
    id: int,
    db: Session = Depends(get_db),
    current_employee: int = Depends(oauth2.get_current_employee)
):
    """ 
    {id} is a path parameter
    """
    # We are
    # - taking an string from the parameter
    # - converting it to int
    # - then again converting it to str
    # We are doing this because we want to valid that the user is giving
    # only integers in the argument and not string like `adfadf`.
    # Plus we are adding a comma after the str(id) because we run into an
    # error later. Don't know the reason for the error yet.
    # post = cursor.fetchone()

    if current_employee.employee_type_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    empl_type = db.query(models.EmployeeType).filter(
        models.EmployeeType.employee_type_id == id
    ).first()

    if not empl_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee Type with id: {id} not found!"
        )

    return empl_type


@router.delete(
    '/delete/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_employee_type(
    id: int,
    db: Session = Depends(get_db),
    current_employee: int = Depends(oauth2.get_current_employee)
):

    if current_employee.employee_type_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    empl_type_query = db.query(models.EmployeeType).filter(
        models.EmployeeType.employee_type_id == id)
    empl_type = empl_type_query.first()

    if empl_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee Type with id: {id} does not exist!"
        )

    empl_type_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# make sure to add some body in the postman to check it.
@router.put(
    '/update/{id}',
    response_model=schemas.EmployeeType
)
def update_empl_type(
    id: int,
    updated_empl_type: schemas.EmployeeTypeCreate,
    db: Session = Depends(get_db),
    current_employee: int = Depends(oauth2.get_current_employee)
):

    if current_employee.employee_type_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    empl_type_query = db.query(
        models.EmployeeType
    ).filter(
        models.EmployeeType.employee_type_id == id
    )

    empl_type = empl_type_query.first()

    if empl_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee Type with id: {id} does not exist!"
        )

    empl_type_query.update(
        updated_empl_type.dict(),
        synchronize_session=False
    )
    db.commit()

    # Sending the updated empl_type back to the user
    return empl_type_query.first()
