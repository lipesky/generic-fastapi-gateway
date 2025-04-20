import asyncio
from patio import Registry, AsyncExecutor
from patio_rabbitmq import RabbitMQBroker

# Criação do registro de serviços
rpc = Registry(project="gateway-ms", auto_naming=False)

# Definição do serviço 'foo'
@rpc("foo")
async def handle_foo(payload):
    print(f"[foo] Recebido: {payload}")
    return 'ZA WARUDO'

async def main():
    # Configuração do broker RabbitMQ
    executor = AsyncExecutor(rpc, max_workers=16)
    await executor.__aenter__()
    
    # Inicialização do broker com o registro de serviços
    broker = RabbitMQBroker(
        executor, amqp_url="amqp://guest:guest@localhost/",
    )
    await broker.__aenter__()

    await broker.join()

    await executor.__aexit__()
    await broker.__aexit__()

if __name__ == "__main__":
    asyncio.run(main())
