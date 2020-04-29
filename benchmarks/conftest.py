import pytest
import redis
import json
import os

def pytest_addoption(parser):
    parser.addoption('--service-name', default='', type=str,
                     help='Redis CF service name')

@pytest.fixture(scope='session')
def redis_client(request):
    config = dict(
        host='redis',
        port=6379,
        password='',
        ssl_cert_reqs=None)

    service_name = request.config.getoption('--service-name')

    try:
        if 'VCAP_SERVICES' in os.environ:
            services = json.loads(os.getenv('VCAP_SERVICES'))
            service_config = services[service_name][0]['credentials']

            if service_config.get('hostname'):
                config['host'] = service_config['hostname']
            else:
                config['host'] = service_config['host']
                config['ssl'] = True

            config['port'] = int(service_config['port'])
            config['password'] = service_config['password']

        client = redis.Redis(**config)
    except redis.ConnectionError:
        client = None

    return client

@pytest.fixture(scope='session')
def clear_redis(redis_client):
    yield redis_client
    redis_client.flushall()
