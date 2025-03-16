import asyncio
from contextvars import ContextVar
from fastapi import APIRouter
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

foo_context: ContextVar[str] = ContextVar("foo", default="bar")

router = APIRouter(prefix="/context")

@router.get("")
async def context_test(var: str):
    foo_context.set(var)
    await asyncio.sleep(1)
    
    return {
        "var": var,
        "context_var": foo_context.get()
    }
    
def send_request(var: str):
    response = requests.get(f"http://localhost:8080/context?var={var}")
    return response.json()

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(send_request, str(i)) for i in range(10)]
        
    for future in as_completed(futures):
        print(future.result())