Microservices project for customers to ask questions and get answers based on reviews.
Here I'm using LLM and RAG locally.
Later I provide docker compose and other scripts.
Also I will update README

To run rabbitmq
```bash
docker run -d \
    --name rabbitmq \
    --hostname rabbitmq \
    -p 15672:15672 \
    -p 5672:5672 \
    rabbitmq:3.10.7-management
```