from faststream.rabbit.fastapi import RabbitRouter
from fastapi import FastAPI
import asyncio
import uuid

app = FastAPI()
router = RabbitRouter()
broker = router.broker
response_futures = {}


@router.post("/get_response")
async def get_response(request: str):
    request_id = str(uuid.uuid4())
    future = asyncio.get_event_loop().create_future()
    response_futures[request_id] = future
    await broker.publish(
        message={
            "question": request,
            "request_id": request_id,
        },
        queue="question_queue",
    )

    try:
        result = await asyncio.wait_for(future, timeout=30)
    except asyncio.TimeoutError:
        del response_futures[request_id]
        return {"status": "timeout"}

    return {"status": "ok", "result": result}


@router.subscriber("messages_response")
async def on_response(data: dict):
    request_id = data.get("request_id")
    result = data.get("result")
    future = response_futures.pop(request_id, None)
    if future:
        future.set_result(result)

app.include_router(router)

