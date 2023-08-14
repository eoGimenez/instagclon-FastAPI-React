from fastapi import APIRouter, Depends, HTTPException, status
from typing_extensions import Annotated
from datetime import timedelta
from schemas.user import UserBase, UserDisplay, UserSignUp
from schemas.token import Token
from config.database import get_db
from config import db_auth
from sqlalchemy.orm.session import Session
from fastapi.security import (
    OAuth2PasswordRequestForm
)
from config.db_user import post_user, get_user_by_id

ACCESS_TOKEN_EXPIRE_MINUTES = 30



router = APIRouter(
    tags=['Authentication']
)

@router.post('/signup', response_model=UserDisplay)
async def create_user(request: UserSignUp, db: Session = Depends(get_db)):
    return post_user(db, request)

@router.get('/{id}', response_model=UserDisplay)
async def get_user(id: int, db: Session = Depends(get_db)):
    return get_user_by_id(db, id)

@router.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    if (len(form_data.scopes) == 1):
        scopes = form_data.scopes[0].split(',')
    if (len(form_data.scopes) == 2):
        scopes = form_data.scopes
    user = db_auth.authenticate_user(
        form_data.username, form_data.password, db
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid credentials')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = db_auth.create_access_token(
        data={'sub': user.username, 'scopes': scopes, 'id': user.id},
        expires_delta=access_token_expires
    )
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user': {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "avatar": user.avatar
        }
    }


@router.get("/users/me/", response_model=UserDisplay)
async def read_users_me(
    current_user: Annotated[UserBase, Depends(db_auth.get_current_active_user)]
):
    return current_user

@router.get("/status/")
async def read_system_status(current_user: Annotated[UserBase, Depends(db_auth.get_current_user)]):
    return {
        "status": "ok",
        "current user": current_user
    }