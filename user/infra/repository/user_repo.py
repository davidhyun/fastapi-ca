from database import SessionLocal
from user.domain.repository.user_repo import IUserRepository
from user.domain.user import User as UserVO
from user.infra.db_models.user import User
from fastapi import HTTPException
from utils.db_utils import row_to_dict

class UserRepository(IUserRepository):
    def save(self, user: UserVO):
        new_user = User(
            id = user.id,
            email = user.email,
            name = user.name,
            password = user.password,
            created_at = user.created_at,
            updated_at = user.updated_at
        )
        
        with SessionLocal() as db:
            try:
                db = SessionLocal() # 새로운 세션을 생성
                db.add(new_user)
                db.commit()
            finally:
                db.close() # (선택사항) with로 세션을 자동으로 닫지만, 처리 과정에서 데이터베이스 에러가 발생했을 때 세션이 제대로 닫히지 않을 수 있는 것을 방지
                
    def find_by_email(self, email: str) -> UserVO:
        with SessionLocal() as db:
            user = db.query(User).filter(User.email == email).first() # 없으면 None 반환
            
        if not user:
            raise HTTPException(status_code=422)
        
        return UserVO(**row_to_dict(user))