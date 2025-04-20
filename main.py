import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, Request, HTTPException
from src.gateway.router.app_router import router as app_routes
from src.settings import get_settings
# Support for cors
# from fastapi.middleware.cors import CORSMiddleware
from patio import NullExecutor, Registry
from patio_rabbitmq import RabbitMQBroker
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(asctime)s - %(message)s')

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.executor = NullExecutor(Registry(project=[settings.broker_project_name]))
    await app.state.executor.__aenter__()
    app.state.broker = RabbitMQBroker(
        app.state.executor, amqp_url=settings.rabbitmq_url, 
    )
    await app.state.broker.__aenter__()
    print('🟢 RabbitMQBroker initialized')
    yield
    await app.state.broker.__aexit__(None, None, None)
    await app.state.executor.__aexit__(None, None, None)

app = FastAPI(
    title="Generic Service",
    lifespan=lifespan,
)

app.include_router(
    app_routes,
    prefix='/api/v1/app',
    tags=['app routes'],
)

# Support for cors
# origins = [
#     "https://example.com.br",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get('/')
async def rootRoute():
    return Response('Generic Service', status_code=200)

@app.get('/healthcheck')
async def healthcheck(request: Request):
    broker: RabbitMQBroker = request.app.state.broker
    if not broker:
        raise HTTPException(status_code=503) # Unavailable
    return Response(status_code=200)

if __name__ == '__main__':
    from uvicorn import run
    import os
    port = settings.port
    if not port:
        port = int(os.environ.get('PORT', '8000' if settings.environment == 'DEV' else '80'))
    run(
        'main:app',
        host='0.0.0.0',
        port=port,
        reload=settings.environment == 'DEV',
        root_path=settings.root_path if settings.root_path else '',
    )
