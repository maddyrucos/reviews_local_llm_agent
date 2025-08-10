To run rabbitmq
```bash
docker run -d \
    --name rabbitmq \
    --hostname rabbitmq \
    -p 15672:15672 \
    -p 5672:5672 \
    rabbitmq:3.10.7-management
```