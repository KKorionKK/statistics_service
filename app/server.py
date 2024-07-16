from fastapi import FastAPI, Request, Response
from jsonrpcserver import Result, Success, async_dispatch, method, Error
from app.common.redis_controller import RedisController
import uvicorn
import json

from common import settings

app = FastAPI()
redis = RedisController()


@method
async def init_stats(context, names: dict[str, str]) -> Result:
    if 'init_stats' in context:
        names_list = list(names.values())
        await redis.init_statistics(names_list)
        return Success(f'Initialized statistics: {names_list}')
    else:
        return Error(message='This method had been disabled.', code=405)

@method
async def increment(context, data: dict[str, str | int]) -> Result:
    if 'increment' in context:
        name = data.get('name')
        value = data.get('value')
        new_value = await redis.increment_statistic(name, value)
        return Success(f'Incremented "{name}" on value {value}. Current value: {new_value}')
    else:
        return Error(message='This method had been disabled.', code=405)

@method
async def get(context, name: str) -> Result:
    if 'get' in context:
        value = await redis.get_statistic(name)
        return Success(value)
    else:
        return Error(message='This method had been disabled.', code=405)


@app.post(settings.SERVER_ENDPOINT)
async def index(request: Request):
    request_json: dict = await request.json()
    response = await async_dispatch(json.dumps(request_json), context=settings.AVAILABLE_METHODS)
    return Response(content=str(response), media_type="application/json")


if __name__ == "__main__":
    uvicorn.run(app, port=settings.SERVER_PORT)
