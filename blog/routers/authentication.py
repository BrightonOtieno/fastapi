from sqlalchemy.orm.session import Session
from blog import models
from blog.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas
from ..database import get_db
from passlib.context import CryptContext
from ..hashing import Hash
from .. import token

router = APIRouter(
    tags=['Authentication'],
)

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"Invalid Credentials"
        )
    # verify password
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"Invalid Credentials, check password & email"
        )
    #TODO: Generate JWT token & return it
    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}
