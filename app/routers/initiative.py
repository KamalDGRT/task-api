from datetime import datetime
from fastapi import status, HTTPException, Response, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, oauth2

# Using hyphen by following this answer
# https://stackoverflow.com/a/18449772
router = APIRouter(
    prefix='/initiative',
    tags=['Initiative']
)


@router.get(
    '/all',
    response_model=List[schemas.InitiativeSimple]
)
# @router.get('/')
def get_initiatives(
    db: Session = Depends(get_db),
):
    results = db.query(models.Initiative).all()
    return results


@router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.InitiativeSimple,
)
def create_initiative(
    status_code: schemas.InitiativeCreate,
    db: Session = Depends(get_db),
    current_employee: int = Depends(oauth2.get_current_employee)
):

    # Allowing only the admins to proceed
    if current_employee.employee_type_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    new_initiative = models.Initiative(
        created_by=current_employee.employee_id,
        updated_by=current_employee.employee_id,
        **status_code.dict(),
    )
    # ** unpacks the dictionary into this format:
    # title=post.title, content=post.content, ...
    # This prevents us from specifiying individual fields

    db.add(new_initiative)
    db.commit()
    db.refresh(new_initiative)

    return new_initiative


@router.get(
    '/info/{id}',
    response_model=schemas.InitiativeComplete
)
def get_initiative(
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

    initiative = db.query(models.Initiative).filter(
        models.Initiative.initiative_id == id
    ).first()

    if not initiative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Initiative with id: {id} not found!"
        )

    return initiative


@router.delete(
    '/delete/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_initiative(
    id: int,
    db: Session = Depends(get_db),
    current_employee: int = Depends(oauth2.get_current_employee)
):

    if current_employee.employee_type_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    initiative_query = db.query(
        models.Initiative
    ).filter(
        models.Initiative.status_id == id
    )
    initiative = initiative_query.first()

    if initiative is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Initiative with id: {id} does not exist!"
        )

    initiative_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# make sure to add some body in the postman to check it.
@router.put(
    '/update/{id}',
    response_model=schemas.InitiativeUpdate
)
def update_initiative(
    id: int,
    updated_initiative: schemas.InitiativeCreate,
    db: Session = Depends(get_db),
    current_employee: int = Depends(oauth2.get_current_employee)
):

    print(updated_initiative)
    if current_employee.employee_type_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    initiative_query = db.query(
        models.Initiative
    ).filter(
        models.Initiative.status_id == id
    )

    initiative = initiative_query.first()

    if initiative is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Initiative Type with id: {id} does not exist!"
        )

    # print(status_code.__dict__)
    updated_init_type = updated_initiative.dict()
    updated_init_type["updated_by"] = current_employee.employee_id
    updated_init_type["updated_at"] = datetime.now().astimezone()

    # print(updated_init_type)
    initiative_query.update(
        updated_init_type,
        synchronize_session=False
    )
    db.commit()

    # Sending the updated empl_type back to the user
    return initiative_query.first()
