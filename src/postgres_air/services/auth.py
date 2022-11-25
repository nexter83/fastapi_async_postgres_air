from datetime import datetime, timedelta
from typing import List

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from passlib.hash import bcrypt
from jose import jwt, JWTError
from pydantic import ValidationError
from starlette import status

from ..database import get_session
from ..schemas.auth import User, Token, UserCreate
from ..models.users import Users
from ..config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign-in")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return AuthService.validate_token(token)


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.user_role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_pasword: str) -> bool:
        return bcrypt.verify(plain_password, hashed_pasword)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate credentials",
            headers={'WWW-Authenticate': 'Bearer'}
        )
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algoritm])
        except JWTError:
            raise exception from None

        user_data = payload.get("user")
        try:
            user = User.parse_obj(user_data)
        except ValidationError:
            raise exception from None
        return user

    @classmethod
    def create_token(cls, user: Users) -> Token:
        user_data = User.from_orm(user)
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expiration),
            'sub': str(user_data.id),
            'user': user_data.dict()
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algoritm
        )
        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(self, user_data: UserCreate) -> Token:
        user = Users(
            email=user_data.email,
            username=user_data.username,
            password_hash=self.hash_password(user_data.password),
            user_role=user_data.user_role.value
        )
        self.session.add(user)
        self.session.commit()
        return self.create_token(user)

    def authenticate_user(self, username: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={'WWW-Authenticate': 'Bearer'}
        )
        user = (
            self.session
            .query(Users)
            .filter(Users.username == username)
            .first()
        )
        if not user or not self.verify_password(password, user.password_hash):
            raise exception
        return self.create_token(user)
