from faststream.rabbit import RabbitBroker
from model import Model
from rag import Retriever
import asyncio

broker = RabbitBroker()
model = Model()
retriever = Retriever()


@broker.subscriber("question_queue")
async def process_message(data: dict):
    question = data.get("question")
    request_id = data.get("request_id")

    if not question or not request_id:
        await broker.publish({'error': 'Invalid request'}, queue="messages_response")
        return

    reviews = retriever.invoke(question)
    result = model.answer_question(question, reviews)

    await broker.publish(
        {"request_id": request_id, "result": result},
        queue="messages_response"
    )


async def main():
    await broker.start()
    while True:
        await asyncio.sleep(3600)



if __name__ == "__main__":
    asyncio.run(main())