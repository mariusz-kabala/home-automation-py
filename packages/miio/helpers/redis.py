# from rediscluster import RedisCluster

# startup_nodes = [{"host": "127.0.0.1", "port": "6379"}]

# rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

import redis
from typing import final

rc = redis.Redis(host='localhost', port=6379, db=0)

PRIMITIVE_TO_STRING: final = {
    True: 'true',
    False: 'false',
    None: 'null'
}

STRING_TO_PRIMITIVE: final = {
    'true': True,
    'false': False,
    'null': None
}

def save_hash(key: str, data):
    for k, v in data.items():
        if type(v) == bool:
            rc.hset(key, k, PRIMITIVE_TO_STRING.get(v))
        elif isinstance(v, int):
            rc.hset(key, k, str(v))
        elif v is None:
            rc.hset(key, k, 'null')
        else:
            rc.hset(key, k, v)

def parse_int(value: str):
    if value == 'null':
        return None
    
    return int(value)

def get_hash(key: str, mapper = None):
    data = rc.hgetall(key)
    result = dict()

    if mapper is not None:
        for k, v in mapper.items():
            index = str.encode(k)
            if v is int:
                result[k] = parse_int(data[index].decode('UTF-8'))
            elif v is bool:
                result[k] = STRING_TO_PRIMITIVE.get(data[index].decode('UTF-8'))
            elif v is str:
                result[k] = data[index].decode('UTF-8')
    else:
        for k, v in data.items():
            index = k.decode('UTF-8')
            if v in STRING_TO_PRIMITIVE:
                result[index] = STRING_TO_PRIMITIVE.get(v.decode('UTF-8'))
            else:
                result[index] = v.decode('UTF-8')

    return result