"""Security Service

Raises:
    HTTPException: 401 - Could not validate credentials
    
Returns:
    function: get_current_user
    function: get_current_active_user
    function: get_password_hash
    function: verify_password
"""
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from src.config import JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY
from src.repository.postgre_repository import PostgreSQLClient, get_db
from src.models.api import UserOut
from src.models.db import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecurityServive:
    def __init__(
        self, postgres_client: Annotated[PostgreSQLClient, Depends(get_db)]
    ) -> None:
        self.db = postgres_client

    def authenticate_user(self, username: str, password: str) -> User | None:
        user = self.db.get_user(username)
        if not user:
            return None
        if not verify_password(password, get_password_hash(password)):
            return None
        return user


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    postgres_client: Annotated[PostgreSQLClient, Depends(get_db)],
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    user = postgres_client.get_user_out(username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: Annotated[UserOut, Depends(get_current_user)]
):
    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        return False


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt
