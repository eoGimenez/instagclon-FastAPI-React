from fastapi import Depends, HTTPException, Security, status
from typing_extensions import Annotated
from typing import Optional
from enviroment.config import Settings, get_settings
from datetime import datetime, timedelta
from sqlalchemy.orm.session import Session
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.models import DbUser
from pydantic import ValidationError
from schemas.user import UserBase, UserToken
from schemas.token import TokenData
from config.database import get_db

dotenv : Settings = get_settings()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='token',
    scopes={'me': 'Read, update, delete information about current user.',
            'post': 'comment, create, update, delete posts and comments'
            },
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hashed(password):
    return pwd_context.hash(password)

def authenticate_user(username:str, password:str, db: Session):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_enconde = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_enconde.update({'exp': expire})
    encode_jwt = jwt.encode(to_enconde, dotenv.secret_key, algorithm=dotenv.algorithm)
    return encode_jwt
    

async def get_current_user(
         security_scoper: SecurityScopes, 
         token: Annotated[str, Depends(oauth2_scheme)],
         db: Session = Depends(get_db)
):
    if security_scoper.scopes:
        authenticate_value = f'Bearer scopre="{security_scoper.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': authenticate_value}
    )
    try:
        payload = jwt.decode(token, dotenv.secret_key, algorithms=[dotenv.algorithm])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_scopes = payload.get('scopes', [])
        token_data = TokenData(scopes=token_scopes, usernam=username)
    except ( JWTError, ValidationError):
        raise credentials_exception
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if user is None:
        raise credentials_exception
    for scope in security_scoper.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='No tienes acceso a esta función',
                headers={'WWW-Authenticate': authenticate_value},
            )
    return user
    
async def get_current_active_user(
        current_user: Annotated[UserToken, Security(get_current_user, scopes=['me'])]
    ):
    if not current_user.active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Inactive user')
    return current_user