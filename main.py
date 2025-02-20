from containers import Container
import uvicorn
from fastapi import FastAPI
from user.interface.controllers.user_controller import router as user_routers
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

app = FastAPI()
app.container = Container()
app.include_router(user_routers)

@app.get("/")
def index():
    return {"message": "Hello, World!"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    # RequestValidationError 예외가 발생했을 때, 400 에러를 반환한다.
    return JSONResponse(
        status_code=400,
        content=exc.errors(),
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
