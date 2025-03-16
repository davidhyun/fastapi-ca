from contextvars import ContextVar

# 유저 활동 추적하는 로깅
# 유저 정보를 콘텍스트 변수로 저장하는 미들웨어
user_context: dict | None = ContextVar("current_usr", default=None)
