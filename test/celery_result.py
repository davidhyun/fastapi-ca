from celery.result import AsyncResult
from common.messaging import celery

if __name__ == "__main__":
    # AsyncResult 첫번째 인수는 Task ID
    async_result = AsyncResult("c58787ae-a384-435d-a395-0f6e14f90dd1", app=celery)
    result = async_result.result
    print(result)