#! usr/bin/python3
# utils/auth_jwt
## Jwt implementation

import bcrypt
import jwt
import binascii
from datetime import datetime, timedelta

SECRET_KEY = "234234-37437y3-435364gr"  # Replace with your actual secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
