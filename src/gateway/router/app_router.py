from fastapi import APIRouter,Request,Depends
from pydantic import BaseModel
from circuitbreaker import circuit
from patio_rabbitmq import RabbitMQBroker

router = APIRouter(
    # dependencies=[
    #     Depends(validate_user)
    # ]
)

class SimpleOperationBody(BaseModel):
    operation: str

count = 0

@circuit
@router.post("/test")
async def test(
    test: SimpleOperationBody, 
    request: Request, 
):
    broker: RabbitMQBroker = request.app.state.broker
    response = await broker.call('foo', 'world')
    return {"status": "ok", "response": response}

@circuit
@router.post("/test-2")
async def test(
    request: Request, 
):
    broker: RabbitMQBroker = request.app.state.broker
    global count
    response = await broker.call(
        'handler', 
        arg1='arg1val count='+str(count), 
        arg2={'1':2}
    )
    count = count + 1
    return {"status": "ok", "response": response}