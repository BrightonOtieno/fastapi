from .. import schemas, models
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException
from ..hashing  import Hash

# password hashing context
#pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(request: schemas.User, db: Session):
    #hashedPassword = pwd_cxt.hash(request.password)
    hashedPassword = Hash.bcrypt(request.password)
    new_user = models.User(
        name=request.name, email=request.email, password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} does not exist")
    return user
