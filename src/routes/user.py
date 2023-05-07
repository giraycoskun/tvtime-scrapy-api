"""User Routes

Raises:
    HTTPException: 400 - Incorrect username or password
    HTTPException: 401 - Invalid credentials

Returns:
    APIRouter: Routes to user actions
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.models.api import UserOut
from src.service.security import (
    authenticate_user,
    create_access_token,
    get_current_user,
)

router = APIRouter(
    prefix="",
    tags=["user"],
    responses={
        200: {"description": "Success"},
    },
)


@router.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # TODO: implement hashing and better password comprarison and token
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(data={"sub": user.username})
    data = {"access_token": token, "token_type": "bearer"}
    return JSONResponse(content=data, status_code=200)


@router.get("/user", summary="Get Data Status")
def get_user(user: Annotated[UserOut, get_current_user]):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return JSONResponse(content=user.dict(), status_code=200)
