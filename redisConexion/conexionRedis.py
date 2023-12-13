import os

import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

print(REDIS_HOST)
print(REDIS_PORT)

dbRedis = redis.Redis(host=str(REDIS_HOST), port=int(REDIS_PORT), db=0)

try:
    dbRedis.ping()
    print('Conexión exitosa a Redis')
except Exception as e:
    print('Error de conexión a Redis', e)

