Python connection to AWS ElastiCache Redis
===========================================

An example app connecting to Redis using [redis-py](https://github.com/andymccurdy/redis-py)

## Migrating from your Redis service

The follow code snippet shows the differences between connecting to the old Redis service
to the new AWS ElastiCache Redis service. The following app code shows how to configure
the Redis client with the Redis service bound to the app. See
[redis-py docs](https://github.com/andymccurdy/redis-py#ssl-connections) for more information.

```python
import os
import json
import redis


##
## The old Redis service `redis32`
##
redis_config = dict()
services = json.loads(os.getenv('VCAP_SERVICES'))
redis_credentials = services['redis32'][0]['credentials']

redis_config['host'] = redis_credentials['hostname'] ## Reassign hostname to host
redis_config['port'] = redis_credentials['port']
redis_config['password'] = redis_credentials['password']

client = redis.Redis(**redis_config)


##
## The new Redis service `redis`
##
redis_config = dict()
services = json.loads(os.getenv('VCAP_SERVICES'))
redis_credentials = services['redis'][0]['credentials']

redis_config['host'] = redis_credentials['host']
redis_config['port'] = redis_credentials['port']
redis_config['password'] = redis_credentials['password']
redis_config['ssl'] = True ## Add the key `ssl` set to `True`
redis_config['ssl_cert_reqs'] = None ## Add the key `ssl_cert_reqs` set to `None`

client = redis.Redis(**redis_config)


## The Redis `client` is ready to be used
```

## Differences in configuration

- The new AWS ElastiCache Redis service credentials has renamed the host name to `host` from `hostname`
- The `ssl` configuration key must be set to `True`
- The `ssl_cert_reqs` configuration key must be set to `None`


## Creating a Redis connection pool

This following example shows how you can use `redis-py` to connect via to the new Redis service through [connection pools](https://github.com/andymccurdy/redis-py#connection-pools). You may choose to do this in order to have precise control of how connections are managed.

```python
from redis import ConnectionPool, SSLConnection
from cfenv import AppEnv

##
## The new Redis service `redis`
## Using `cfenv` module to grab the Redis service from VCAP_SERVICES
##
redis_service = cfenv.get_service(label=re.compile("redis.*"))

## Instantiate the Redis connection pool
connection_pool = ConnectionPool(
    host=redis_service.credentials["host"],
    port=redis_service.credentials["port"],
    password=redis_service.credentials["password"],
    ssl=True,
    ssl_cert_reqs=None,
    connection_class=SSLConnection
)

## The Redis `connection_pool` is ready to be used
```
