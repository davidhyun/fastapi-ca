from datetime import datetime
from dependency_injector.wiring import inject, Provide
from containers import Container
from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr, Field
from user.application.user_service import UserService

router = APIRouter(prefix="/users")

class CreateUserBody(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=8, max_length=32)

class UpdateUser(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=32, default=None)

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: datetime

class GetUsersResponse(BaseModel):
    total_count: int
    page: int
    users: list[UserResponse]

@router.post("", status_code=201, response_model=UserResponse) # 201: 요청이 성공적으로 처리되어 리소스가 만들어졌음
@inject
def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    created_user = user_service.create_user(
        name = user.name,
        email = user.email,
        password = user.password
    )
    return created_user

@router.put("/{user_id}")
@inject
def update_user(
    user_id: str,
    user: UpdateUser,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    user = user_service.update_user(
        user_id = user_id,
        name = user.name,
        password = user.password
    )
    
    return user

@router.get("", response_model=GetUsersResponse)
@inject
def get_users(
    page: int = 1,
    items_per_page: int = 10,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    total_count, users = user_service.get_users(page, items_per_page)
    
    return {
        "total_count": total_count,
        "page": page,
        "users": users
    }
    
@router.delete("", status_code=204) # 204: 요청이 성공적으로 처리되었지만 콘텐츠가 없음
@inject
def delete_user(
    user_id: str,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    # TODO: 다른 유저를 삭제할 수 없도록 토큰에서 유저 아이디를 구한다.
    user_service.delete_user(user_id)