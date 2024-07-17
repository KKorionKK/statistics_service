import redis.asyncio as redis
from redis.asyncio.client import Pipeline

from app.common import settings as s
from jsonrpcserver import JsonRpcError


class RedisController:
    def __init__(self):
        self.redis = redis.Redis(
            host=s.REDIS_HOST,
            port=s.REDIS_PORT,
            password=s.REDIS_PASSWORD,
            username=s.REDIS_USERNAME
        )

    async def if_statistic_exist(self, name: str):
        res = await self.redis.get(name)
        if res is None:
            return False
        else:
            return True

    async def __get_statistic(self, name: str):
        res = await self.redis.get(name)
        if res:
            return int(res)
        return res

    async def get_statistic(self, name: str):
        if await self.if_statistic_exist(name):
            return await self.__get_statistic(name)
        else:
            raise JsonRpcError(400, f'Statistics with name "{name}" have not initialized yet.')

    async def init_statistics(self, names: list[str]):
        errors: list[str] = []
        pipeline: Pipeline = self.redis.pipeline()
        for name in names:
            if await self.if_statistic_exist(name):
                errors.append(name)
                continue
            pipeline.set(name, 0)
        if errors:
            raise JsonRpcError(400, f'The following statistics have already been initialized: {errors}. Operation cancelled.')
        await pipeline.execute(True)

    async def increment_statistic(self, name: str, value: int):
        if await self.if_statistic_exist(name):
            await self.redis.incr(name, value)
        else:
            raise JsonRpcError(400, f'Statistics with name "{name}" have not initialized yet. Operation cancelled.')
        return await self.__get_statistic(name)






