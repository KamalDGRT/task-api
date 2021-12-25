from datetime import datetime
from fastapi import status, HTTPException, Response, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, oauth2

# Using hyphen by following this answer
# https://stackoverflow.com/a/18449772
router = APIRouter(
    prefix='/rating',
    tags=['Rating']
)


@router.get(
    '/all',
    response_model=List[schemas.RatingSimple]
)
# @router.get('/')
def get_ratings(
    db: Session = Depends(get_db),
):
    results = db.query(models.Rating).all()
    return results


@router.get(
    '/all/initiative/{id}',
    response_model=List[schemas.RatingSimple]
)
# @router.get('/')
def get_all_ratings_for_a_initiative(
    id: int,
    db: Session = Depends(get_db),
):
    results = db.query(models.Rating).filter(
        models.Rating.initiative_id == id
    ).all()
    return results


@router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.RatingSimple,
)
def create_rating(
    rating: schemas.RatingCreate,
    db: Session = Depends(get_db),
    current_employee: int = Depends(oauth2.get_current_employee)
):

    new_rating = models.Rating(
        given_by=current_employee.employee_id,
        **rating.dict(),
    )
    # ** unpacks the dictionary into this format:
    # title=post.title, content=post.content, ...
    # This prevents us from specifiying individual fields

    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)

    return new_rating


@router.get(
    '/info/{id}',
    response_model=schemas.RatingComplete
)
def get_rating(
    id: int,
    db: Session = Depends(get_db),
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

    rating = db.query(models.Rating).filter(
        models.Rating.rating_id == id
    ).first()

    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rating with id: {id} not found!"
        )

    return rating


@router.delete(
    '/delete/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_rating(
    id: int,
    db: Session = Depends(get_db),
    current_employee: int = Depends(oauth2.get_current_employee)
):

    rating_query = db.query(
        models.Rating
    ).filter(
        models.Rating.rating_id == id
    )
    rating = rating_query.first()

    if rating is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rating with id: {id} does not exist!"
        )

    if current_employee.employee_id != rating.given_by:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    rating_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# make sure to add some body in the postman to check it.
@router.put(
    '/update/{id}',
    response_model=schemas.RatingUpdate
)
def update_rating(
    id: int,
    updated_rating: schemas.RatingCreate,
    db: Session = Depends(get_db),
    current_employee: int = Depends(oauth2.get_current_employee)
):

    rating_query = db.query(
        models.Rating
    ).filter(
        models.Rating.rating_id == id
    )

    rating = rating_query.first()

    if rating is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rating with id: {id} does not exist!"
        )

    if current_employee.employee_id != rating.given_by:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    # print(status_code.__dict__)
    updated_init_type = updated_rating.dict()
    updated_init_type["updated_at"] = datetime.now().astimezone()

    # print(updated_init_type)
    rating_query.update(
        updated_init_type,
        synchronize_session=False
    )
    db.commit()

    # Sending the updated empl_type back to the user
    return rating_query.first()
