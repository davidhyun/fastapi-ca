import time
from fastapi import FastAPI, Request

def create_middleware(app: FastAPI):
    
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time) # 커스텀 헤더에는 보통 X-를 붙임
        
        return response