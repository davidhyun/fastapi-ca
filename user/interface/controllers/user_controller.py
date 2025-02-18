from fastapi import APIRouter
from pydantic import BaseModel
from user.application.user_service import UserService

router = APIRouter(prefix="/users")

class CreateUserBody(BaseModel):
    name: str
    email: str
    password: str

@router.post("", status_code=201) # 201: 요청이 성공적으로 처리되어 리소스가 만들어졌음
def create_user(user: CreateUserBody):
    user_service = UserService()
    created_user = user_service.create_user(
        name = user.name,
        email = user.email,
        password = user.password
    )
    return created_user