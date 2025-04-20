# Generic Fastapi/RabbitMQ Gateway Server

This repository holds the code for a blank microservice that uses patio, rabbitmq in an async approach to handle requests and distributes to processing microsservices in request-reply approach, with distributed rpc calls thanks to patio.

You can use this as basis for other gateway microservices.

The example sends request to queue to be consumed by [Generic consumer](https://github.com/lipesky/generic-fastapi-rabbitmq-consumer)

Pull requests are welcome.
