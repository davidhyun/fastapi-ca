from ulid import ULID
from datetime import datetime
from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository
from user.infra.repository.user_repo import UserRepository
from fastapi import HTTPException
from utils.crypto import Crypto

class UserService:
    def __init__(self):
        self.user_repo: IUserRepository = UserRepository()
        self.ulid = ULID()
        self.crypto = Crypto()
        
    def create_user(self, name: str, email: str, password: str):
        _user = None # 데이터베이스에서 찾은 유저 변수. 새로 생성할 유저와 구분하기 위해 _를 붙임

        try:
            _user = self.user_repo.find_by_email(email)
        except HTTPException as e:
            if e.status_code != 422:
                raise e
            
        if _user:
            raise HTTPException(status_code=422)
        
        now = datetime.now()
        user: User = User(
            id = self.ulid.generate(),
            name = name,
            email = email,
            password = self.crypto.encrypt(password),
            created_at = now,
            updated_at = now
        )
        self.user_repo.save(user)
        
        return user