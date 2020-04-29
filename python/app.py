from flask import Flask
import os
import redis
import json

app = Flask(__name__)

# Get port from environment variable or choose 8080 as local default
port = int(os.getenv("PORT", 8080))

# Get Redis credentials from CF service
if 'VCAP_SERVICES' in os.environ:
    services = json.loads(os.getenv('VCAP_SERVICES'))
    aws_redis_config = services['redis'][0]['credentials']
    aws_redis_config['port'] = int(aws_redis_config['port'])
    del aws_redis_config['uri']
else:
    aws_redis_config = dict(hostname='localhost', port=6379, password='')

# Connect to redis
try:
    client = redis.Redis(**aws_redis_config, ssl_cert_reqs=None, ssl=True)
except redis.ConnectionError:
    client = None

print(vars(client))

@app.route('/')
def keys():
    try:
        hits = client.incr('hits')
        keys = client.keys('*')
        return f'Hits: {hits}\nKeys: {keys}'
    except Exception as error:
        print(error)
        return 'Error'

@app.route('/<key>')
def get_current_values(key):
    try:
        result = client.lrange(key, 0, -1)
        message = f'Values: {str(result)}'
        return message
    except Exception as error:
        print(error)
        return 'Error'

@app.route('/<key>/<s>')
def add_value(key, s):
    try:
        client.rpush(key, s)
        return f'Added {s} to {key}.'
    except Exception as error:
        print(error)
        return 'Error'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
