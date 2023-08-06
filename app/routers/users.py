from .. import models, schemas, utils
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
   
router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# ================================================================================================
#create user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutput)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #hashing password
    # declare variable to take hash function inside utils.py file and save it to database as hashed password
    hashed_pwd = utils.hash(user.password) 
    user.password = hashed_pwd

    new_user = models.User(**user.dict()) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# ================================================================================================
#get user
@router.get("/{id}", response_model=schemas.UserOutput)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} doesnt exists")
    
    return user    