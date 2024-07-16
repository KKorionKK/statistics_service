import os
from dotenv import find_dotenv, dotenv_values

env = dotenv_values(os.getcwd() + '/common/global_configs/prod.env')
print(os.getcwd() + '/common/global_configs/prod.env')

AVAILABLE_METHODS = ['init_stats', 'increment', 'get']

REDIS_HOST = env.get('REDIS_HOST')
REDIS_PORT = int(env.get('REDIS_PORT'))
REDIS_USERNAME = env.get('REDIS_USERNAME')
REDIS_PASSWORD = env.get('REDIS_PASSWORD')

SERVER_ENDPOINT = env.get('SERVER_ENDPOINT')
SERVER_PORT = int(env.get('SERVER_PORT'))