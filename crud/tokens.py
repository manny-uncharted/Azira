# crud/tokens.py
from sqlalchemy.orm import Session
from models.tokens import Token
from models.users import User
from schemas.tokens import TokenCreate

def create_user_token(db: Session, token, user_id: int):
    db_token = Token(access_token=token, user_id=user_id)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def get_token_by_user_id(db: Session, user_id: int):
    return db.query(Token).filter(Token.user_id == user_id).first()

def get_user_token(db: Session, token:str):
    return db.query(Token).filter(Token.access_token == token).first()

def update_user_token(db: Session, token_id: int, new_token: str):
    db_token = db.query(Token).filter(Token.id == token_id).first()
    if db_token:
        db_token.access_token = new_token
        db.commit()
        db.refresh(db_token)
        return db_token
    return None

def delete_user_token(db: Session, token_id: int):
    db_token = db.query(Token).filter(Token.id == token_id).first()
    if db_token:
        db.delete(db_token)
        db.commit()
        return True
    return False
