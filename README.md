# 백엔드 서버 기동
```bash
$ uvicorn main:app --reload --port 8080
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