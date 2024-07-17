from jsonrpcserver import Result, Success, async_dispatch, method, Error
from app.common.redis_controller import RedisController
from aiohttp import web

from common import settings

redis = RedisController()


@method
async def init_stats(context, *args) -> Result:
    names = list(args)
    if 'init_stats' in context:
        await redis.init_statistics(names)
        return Success(f'Initialized statistics: {names}')
    else:
        return Error(message='This method has been disabled.', code=405)


@method
async def increment(context, data: dict[str, str | int]) -> Result:
    if 'increment' in context:
        name = data.get('name')
        value = data.get('value')
        new_value = await redis.increment_statistic(name, value)
        return Success(f'Incremented "{name}" on value {value}. Current value: {new_value}')
    else:
        return Error(message='This method has been disabled.', code=405)


@method
async def get(context, name: str) -> Result:
    if 'get' in context:
        value = await redis.get_statistic(name)
        return Success(value)
    else:
        return Error(message='This method has been disabled.', code=405)


async def handle_request(request):
    return web.Response(
        text=await async_dispatch(await request.text(), context=settings.AVAILABLE_METHODS),
        content_type='application/json'
    )


app = web.Application()
app.router.add_post(settings.SERVER_ENDPOINT, handle_request)

if __name__ == "__main__":
    web.run_app(app, port=settings.SERVER_PORT)
