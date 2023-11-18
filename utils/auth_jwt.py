#! usr/bin/python3
# utils/auth_jwt
## Jwt implementation

import os
import bcrypt
import jwt
import binascii
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.environ.get("SECRET")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE")

# Utility function to hash passwords
def create_hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Utility function to verify passwords
def verify_password(plain_password, hashed_password):
    if not isinstance(plain_password, bytes):
        plain_password = plain_password.encode('utf-8')

    # Convert the hexadecimal string to bytes if necessary
    if isinstance(hashed_password, str) and hashed_password.startswith("\\x"):
        hashed_password = binascii.unhexlify(hashed_password[2:])

    validator = bcrypt.checkpw(plain_password, hashed_password)
    print(f"Validator check: {validator}")
    return validator


# Utility function to generate JWT tokens
def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
