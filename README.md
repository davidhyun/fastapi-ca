# 도메인 주도 개발 (DDD)
- 클린 아키텍처는 계층형 아키텍처에서 발전된 형태이다. 계층을 완전히 별개로 보면 모든 통신을 인터페이스로 해야 하고, 구조가 너무 복잡해진다.
- **Domain**: 핵심 비즈니스 규칙, 도메인 객체, Repository 인터페이스
- **Application**: Use Case 구현, 도메인 로직을 호출하고 트랜잭션 단위/흐름 관리
- **Interface**: 사용자의 요청/응답을 처리하는 입출력 계층 (Controller 등)
- **Infra**: DB/외부 API 등 실제 구현, Domain에서 정의한 인터페이스 구현체

## 1. Domain 계층
#### 주요 역할
- 핵심 비즈니스 로직과 도메인 모델이 위치하는 계층
- 애플리케이션의 ‘문제 영역’(User, Order, Product 등)에 대한 규칙/규약/개념을 정의
- 도메인 객체(엔티티, 밸류 오브젝트), 도메인 서비스 등을 포함

#### domain/repository/user_repo.py (예시)
- Repository 인터페이스 또는 추상 클래스 형태로, “사용자를 어떻게 영속화할 것인지”에 대한 규약만 정의
- 예: UserRepository 인터페이스를 정의하고, create_user(user), find_by_id(user_id) 같은 메서드 시그니처만 명시
- 구현체는 infra 계층에서 담당

#### domain/user.py
- 도메인 엔티티(User) 혹은 밸류 오브젝트를 정의
- 사용자와 관련된 핵심 속성(id, name, email 등) 및 불변 조건, 도메인 로직(예: 사용자 이름 변경 규칙 등)을 작성

## 2. Application 계층
#### 주요 역할
- Use Case(업무 시나리오)를 구현
- 도메인 로직을 호출하여 처리하고, 트랜잭션 단위 등을 관리
- 복잡한 비즈니스 규칙은 최대한 Domain에 위임하고, “어떤 순서로 무엇을 호출해야 하는지”와 같은 애플리케이션 로직을 담당
- 외부로부터 받은 요청(Interface 계층에서 들어온 요청)을 도메인 계층의 기능과 연결

#### application/user_service.py (예시)
- 사용자와 관련된 Use Case(예: 회원가입, 회원정보 변경 등)를 담당하는 서비스 클래스
- domain 계층의 UserRepository(인터페이스) 및 User(엔티티)를 사용해서 비즈니스 로직을 수행
- 트랜잭션 단위로 메서드를 구성하거나, 여러 도메인 객체를 조합해 업무 로직을 수행

## 3. Infra(InfraStructure) 계층
#### 주요 역할
- 데이터베이스, 외부 API, 메시지 브로커 등 인프라스트럭처와의 연동 담당
- domain 계층에서 정의한 Repository 인터페이스의 구현체가 위치
- ORM(Entity Framework, SQLAlchemy 등) 모델, DB 커넥션, 외부 서비스 연동 로직 등이 포함

#### infra/db_models/user.py (예시)
- 실제 ORM 모델 클래스 정의
- 예: SQLAlchemy 사용 시 Base를 상속한 UserModel, 컬럼 정의 등

#### infra/repository/user_repo.py
- domain 계층에 있는 UserRepository 인터페이스를 구현하는 클래스
- 실제 DB 접근 코드, ORM을 이용한 CRUD 로직 등이 들어감
- 예: SQLAlchemyUserRepository(UserRepository) 같은 형태

## 4. Interface 계층
#### 주요 역할
- 프레젠테이션 혹은 입출력 담당
- 웹이라면 Controller(혹은 View), CLI라면 CLI Handler, 모바일/데스크톱이라면 그에 맞는 어댑터가 위치
- 사용자의 요청을 받아서 Application 계층으로 전달하고, 응답을 다시 사용자에게 반환

#### interface/controllers/user_controller.py
- 예: Flask, FastAPI, Django 등의 웹 프레임워크에서 라우팅, HTTP 요청/응답을 처리
- 들어온 HTTP 요청을 Application 계층(user_service)으로 넘겨서 Use Case를 수행
- 결과를 JSON, HTML 등으로 직렬화하여 클라이언트에게 전달


# 백엔드 서버 기동
```bash
$ uvicorn main:app --reload --port 8080

# OpenAPI 문서: http://localhost:8080/docs
```

# DB 접속
```bash
# 컨테이너 접속
$ docker exec -it mysql-local bash

# DB 접속
$ mysql -u root -p
```

# 회원 가입 유스 케이스

회원 가입 기능에 대한 요구 사항

1. 전달받은 이메일과 패스워드를 User 테이블에 저장한다.
2. 이 때 중복된 이메일이 존재한다면 에러를 발생시킨다.
3. 패스워드는 사람이 읽지 못하게 암호화돼야 한다.

# 데이터베이스 사용하기

- 객체 관계 매핑(ORM)은 데이터베이스와 객체 지향 프로그래밍 언어 간의 데이터 변환을 도와주는 기술
- 특정 데이터베이스에 종속되지 않아 프로그램 이식하기 용이

```bash
# SQLAlchemy 관련 패키지 설치
$ poetry add sqlalchemy mysqlclient alembic

# Alembic으로 테이블 생성 및 리비전 관리
$ alembic init migrations

# Alembic이 현재 소스와 alembic_version 테이블을 비교해 자동으로 리비전 파일 생성
$ alembic revision --autogenerate -m "add User Table"

# 가장 최신의 리비전 파일까지 마이그레이션 수행
$ alembic upgrade head

# 가장 최근의 리비전으로 롤백
$ alembic downgrade -1

# 데이터베이스에서 alembic version 테이블 조회
$ SELECT * FROM alembic _version;
```

# 유저 추가
```bash
$ curl -X 'POST' \
'http://127.0.0.1:8080/users' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
"name": "Dexter",
"email": "dexter.haan@gmail.com",
"password": "Test1234"
}'
```

```python
from database import SessionLocal
from user.infra.db_models.user import User
from datetime import datetime
from utils.crypto import Crypto

with SessionLocal() as db:
    for i in range(50):
        user = User(
            id=f"UserID-{str(i).zfill(2)}",
            name=f"TestUser{i}",
            email=f"test-user{i}@test.com",
            password=Crypto().encrypt("test"),
            memo=None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(user)
    db.commit()
```

# 유저 정보(이름) 변경
```bash
$ curl -X 'PUT' \
'http://localhost:8080/users/01JMCNGWF4W7PYPM333TGXH675' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
  "name": "Dexter NEW"
}'
```

# 유저 목록 조회 (Paging)
```bash
$ curl -X GET 'http://localhost:8080/users?page=2&items_per_page=3'
```

# 유저 삭제
```bash
$ curl -X DELETE 'http://localhost:8080/users?user_id=UserID-02'
$ curl -X GET 'http://localhost:8080/users?page=2&items_per_page=2
```

# 유효성 검사 (Pydantic)
```bash
$ curl -X POST \
'http://localhost:8080/users' \
-H 'Content-Type: application/json' \
-d '{
    "name": "김수한무거북이와 두루미 삼천갑자 동방삭 치치치치치치치치치치치치치치치치치치치치치치치치치치치치치치치치치치치치칯치치치",              
    "email": "normal_string",
    "password": "짧은비번"
}'
```

# 로그인
```bash
$ curl -X POST 'http://localhost:8080/users/login' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-d 'username=dexter.haan@gmail.com&password=Test1234'
```

# 유저 정보 업데이트
```bash
$ curl -X PUT 'http://localhost:8080/users' \
-H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMDFKTUNOR1dGNFc3UFlQTTMzM1RHWEg2NzUiLCJyb2xlIjoiVVNFUiIsImV4cCI6MTc0MDIyMjQ4MH0.BIqrd1g5SKcXFcTp32nbFVIL6X0lN8v4RQwo1bCbfjk' \
-H 'Content-Type: application/json' \
-d '{"name": "Dexter NEW2"}'
```