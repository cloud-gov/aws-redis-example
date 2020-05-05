import pytest
import random


def benchmark_ping(benchmark, redis_client):
    benchmark(redis_client.ping)


def benchmark_set(benchmark, redis_client):
    benchmark(redis_client.set, 'test', random.choice(['win', 'lose', 'draw']))


def benchmark_get(benchmark, redis_client):
    benchmark(redis_client.get, 'test')


def benchmark_keys(benchmark, redis_client):
    benchmark(redis_client.keys, '*')
