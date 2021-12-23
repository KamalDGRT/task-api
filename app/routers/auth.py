from fastapi import APIRouter,  Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(tags=['Authentication'])


@router.post(
    '/login',
    response_model=schemas.Token
)
def login(
    employee_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    employee = db.query(models.Employee).filter(
        models.Employee.email == employee_credentials.username
    ).first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials !!!"
        )

    # if the passwords do not match
    if not utils.verify(
        employee_credentials.password,
        employee.password
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials !!!"
        )

    # Create a Token & return it
    access_token = oauth2.create_access_token(
        data={
            "employee_id": employee.employee_id
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
