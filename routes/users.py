#! usr/bin/python3
# routes/users.py

from fastapi import APIRouter, Depends, HTTPException, status, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


# local imports
from models.users import User
from schemas.users import UserCreate, User as UserSchema
from schemas.tokens import TokenCreate, Token as TokenSchema
from models.tokens import Token
from crud.users import create_user, get_user
from crud.tokens import create_user_token, get_token_by_user_id
from utils.auth_jwt import create_hash_password, create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from middleware.middleware import get_db
import db.db as DB
from utils.bg_tasks import update_user_token_every_30_mins

DB.Base.metadata.create_all(bind=DB.engine)

router = APIRouter()

@router.post('/register')
def register_user(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # create jwt token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    # Set cookies with expiry
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", expires=ACCESS_TOKEN_EXPIRE_MINUTES*60)
    response.set_cookie(key="client_id", value=user.username, expires=ACCESS_TOKEN_EXPIRE_MINUTES*60)
    
    try:
        created_user = create_user(db=db, user=user)
        create_user_token(db=db, token=access_token, user_id=created_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")

    return {"message": "User registered successfully"}


@router.post('/login')
def get_user_and_login(user: UserCreate, response: Response, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Check if the user exists in the database
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Verify the password
    pass_verify = verify_password(user.password, db_user.hashed_password)
    if not pass_verify:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # If both username and password are correct, proceed with login
    try:
        user_access_token = get_token_by_user_id(db=db, user_id=db_user.id)
        # Start the background task
        # background_tasks.add_task(update_user_token_every_30_mins, db, db_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during login: {str(e)}")

    return {
        "message": f"User {db_user.username} logged in successfully",
        "access_token": user_access_token,
        "token_type": "bearer"
    }
        