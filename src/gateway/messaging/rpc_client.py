import asyncio
from patio import Registry
from patio_rabbitmq import RabbitMQBroker

# Criação do registro de serviços
rpc = Registry()

if __name__ == "__main__":
    async def main():
        # Configuração do broker RabbitMQ
        broker = RabbitMQBroker("amqp://guest:guest@localhost/")
        
        # Inicialização do broker com o registro de serviços
        await broker.start(rpc)
        
        # Chamada RPC para o serviço 'foo' com dados de exemplo
        response = await broker.call("foo", {"msg": "olá"})
        print("Resposta:", response)
    asyncio.run(main())
