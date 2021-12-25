from datetime import datetime
from fastapi import status, HTTPException, Response, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, oauth2

# Using hyphen by following this answer
# https://stackoverflow.com/a/18449772
router = APIRouter(
    prefix='/task-log',
    tags=['Task Logs']
)


@router.get(
    '/all',
    response_model=List[schemas.TaskLogSimple]
)
# @router.get('/')
def get_task_logs(
    db: Session = Depends(get_db),
):
    results = db.query(models.TaskLog).all()
    return results


@router.get(
    '/all/initiative/{id}',
    response_model=List[schemas.TaskLogSimple]
)
# @router.get('/')
def get_task_logs_for_a_initiative(
    id: int,
    db: Session = Depends(get_db),
):
    results = db.query(models.TaskLog).filter(
        models.TaskLog.initiative_id == id
    ).all()
    return results


@router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.TaskLogSimple,
)
def create_task_log(
    task_log: schemas.TaskLogCreate,
    db: Session = Depends(get_db),
    current_employee: int = Depends(oauth2.get_current_employee)
):

    new_task_log = models.TaskLog(
        logged_by=current_employee.employee_id,
        **task_log.dict(),
    )
    # ** unpacks the dictionary into this format:
    # title=post.title, content=post.content, ...
    # This prevents us from specifiying individual fields

    db.add(new_task_log)
    db.commit()
    db.refresh(new_task_log)

    return new_task_log


@router.get(
    '/info/{id}',
    response_model=schemas.TaskLogComplete
)
def get_task_log(
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

    task_log = db.query(models.TaskLog).filter(
        models.TaskLog.task_id == id
    ).first()

    if not task_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TaskLog with id: {id} not found!"
        )

    return task_log


@router.delete(
    '/delete/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task_log(
    id: int,
    db: Session = Depends(get_db),
    current_employee: int = Depends(oauth2.get_current_employee)
):

    task_log_query = db.query(
        models.TaskLog
    ).filter(
        models.TaskLog.task_id == id
    )
    task_log = task_log_query.first()

    if task_log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task Log with id: {id} does not exist!"
        )

    if current_employee.employee_id != task_log.logged_by:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    task_log_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# make sure to add some body in the postman to check it.
@router.put(
    '/update/{id}',
    response_model=schemas.TaskLogUpdate
)
def update_task_log(
    id: int,
    updated_task_log: schemas.TaskLogCreate,
    db: Session = Depends(get_db),
    current_employee: int = Depends(oauth2.get_current_employee)
):

    task_log_query = db.query(
        models.TaskLog
    ).filter(
        models.TaskLog.task_id == id
    )

    task_log = task_log_query.first()

    if task_log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task log with id: {id} does not exist!"
        )

    if current_employee.employee_id != task_log.logged_by:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action!"
        )

    # print(status_code.__dict__)
    updated_init_type = updated_task_log.dict()
    updated_init_type["updated_at"] = datetime.now().astimezone()

    # print(updated_init_type)
    task_log_query.update(
        updated_init_type,
        synchronize_session=False
    )
    db.commit()

    # Sending the updated empl_type back to the user
    return task_log_query.first()
