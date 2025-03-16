from config import get_settings
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from enum import StrEnum
from dataclasses import dataclass
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated


settings = get_settings()

SECRET_KEY = settings.jwt_secret
ALGORITHM = "HS256"

oauth2_shceme = OAuth2PasswordBearer(tokenUrl="/users/login")

class Role(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"


@dataclass
class CurrentUser:
    id: str
    role: Role
    
    # LogRecord 객체의 user 속성은 log_format에 사용되는 문자열
    # 콘텍스트 변수에서 가져온 CurrentUser 객체를 문자열로 변환해주어야 한다
    def __str__(self):
        return f"{self.id}({self.role})"

def get_current_user(token: Annotated[str, Depends(oauth2_shceme)]):
    payload = decode_access_token(token)
    
    user_id = payload.get("user_id")
    role = payload.get("role")
    
    if not user_id or not role or role != Role.USER:
        # user_id가 없거나 role이 없거나 role이 USER가 아닌 경우 "403 권한 에러 발생"
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return CurrentUser(user_id, Role(role))


def get_admin_user(token: Annotated[str, Depends(oauth2_shceme)]):
    payload = decode_access_token(token)
    
    role = payload.get("role")
    if not role or role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def create_access_token(payload:dict, role: Role, expires_delta: timedelta=timedelta(hours=6)):
    expire = datetime.now(timezone.utc) + expires_delta
    payload.update({"role": role, "exp": expire})
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)