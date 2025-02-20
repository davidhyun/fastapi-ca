from dataclasses import dataclass
from datetime import datetime

@dataclass
class Profile:
    # 데이터만 가지고 있는 도메인 객체 (Value Object)
    # 데이터베이스에서도 도메인을 분리하여 Profile 테이블을 만들 필요는 없음 (선택 사항)
    name: str
    email: str

@dataclass
class User:
    id: str
    # profile: Profile # User의 도메인 속성을 Profile로 분리 가능
    name: str
    email: str
    password: str
    memo: str | None
    created_at: datetime
    updated_at: datetime