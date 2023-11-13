#!usr/bin/python3
# utils/bg_tasks

from sqlalchemy.orm import Session
import time

#Local imports
from crud.tokens import create_user_token, update_user_token


def update_user_token_every_30_mins(db: Session, user_id: int):
    while True:
        time.sleep(1800)  # Sleep for 30 minutes
        # Logic to create a new token and update it in the database
        new_access_token = create_user_token(data={"sub": user_id})
        update_user_token(db, user_id, new_access_token)
        # Make sure to handle database session and exceptions appropriately
