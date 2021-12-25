from datetime import datetime
from fastapi import status, HTTPException, Response, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, oauth2

# Using hyphen by following this answer
# https://stackoverflow.com/a/18449772
router = APIRouter(
    prefix='/review',
    tags=['Review']
)


@router.get(
    '/all',
    response_model=List[schemas.ReviewSimple]
)
# @router.get('/')
def get_reviews(
    db: Session = Depends(get_db),
):
    results = db.query(models.Review).all()
    return results


@router.get(
    '/all/initiative/{id}',
    response_model=List[schemas.ReviewSimple]
)
# @router.get('/')
def get_all_reviews_for_a_initiative(
    id: int,
    db: Session = Depends(get_db),
):
    results = db.query(models.Review).filter(
        models.Review.initiative_id == id
    ).all()
    return results


@router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ReviewSimple,
)
def create_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_employee: int = Depends(oauth2.get_current_employee)
):

    new_review = models.Review(
        given_by=current_employee.employee_id,
        **review.dict(),
    )
    # ** unpacks the dictionary into this format:
    # title=post.title, content=post.content, ...
    # This prevents us from specifiying individual fields

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review


@router.get(
    '/info/{id}',
    response_model=schemas.ReviewComplete
)
def get_review(
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

    review = db.query(models.Review).filter(
        models.Review.review_id == id
    ).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id: {id} not found!"
        )

    return review


@router.delete(
    '/delete/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_review(
    id: int,
    db: Session = Depends(get_db),
    current_employee: int = Depends(oauth2.get_current_employee)
):

    review_query = db.query(
        models.Review
    ).filter(
        models.Review.review_id == id
    )
    review = review_query.first()

    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id: {id} does not exist!"
        )

    if current_employee.employee_id != review.given_by:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    review_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# make sure to add some body in the postman to check it.
@router.put(
    '/update/{id}',
    response_model=schemas.ReviewUpdate
)
def update_review(
    id: int,
    updated_review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_employee: int = Depends(oauth2.get_current_employee)
):

    review_query = db.query(
        models.Review
    ).filter(
        models.Review.review_id == id
    )

    review = review_query.first()

    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id: {id} does not exist!"
        )

    if current_employee.employee_id != review.given_by:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    # print(status_code.__dict__)
    updated_init_type = updated_review.dict()
    updated_init_type["updated_at"] = datetime.now().astimezone()

    # print(updated_init_type)
    review_query.update(
        updated_init_type,
        synchronize_session=False
    )
    db.commit()

    # Sending the updated empl_type back to the user
    return review_query.first()
