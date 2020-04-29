import pytest
import random

@pytest.mark.benchmark(group="redis-ping")
def benchmark_ping(benchmark, redis_client):
    benchmark(redis_client.ping)

@pytest.mark.benchmark(group="redis-set")
def benchmark_set(benchmark, redis_client):
    benchmark(redis_client.set, 'test', random.choice(['win', 'lose', 'draw']))

@pytest.mark.benchmark(group="redis-get")
def benchmark_get(benchmark, redis_client):
    benchmark(redis_client.get, 'test')

@pytest.mark.benchmark(group="redis-keys")
def benchmark_keys(benchmark, redis_client):
    benchmark(redis_client.keys, '*')
