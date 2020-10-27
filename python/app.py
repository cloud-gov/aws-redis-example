from flask import Flask
import os
import redis
import json

app = Flask(__name__)

# Get port from environment variable or choose 8080 as local default
port = int(os.getenv('PORT', 8080))

redis_config = dict(host='localhost', port=6379, password='')

# Get Redis credentials from CF service
if 'VCAP_SERVICES' in os.environ:
    services = json.loads(os.getenv('VCAP_SERVICES'))
    redis_credentials = services['aws-elasticache-redis'][0]['credentials']

    redis_config['host'] = redis_credentials['host']
    redis_config['port'] = int(redis_credentials['port'])
    redis_config['password'] = redis_credentials['password']
    redis_config['ssl'] = True
    redis_config['ssl_cert_reqs'] = None

# Connect to redis
try:
    client = redis.Redis(**redis_config)
except redis.ConnectionError:
    client = None

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
        result = client.mget(key)
        message = f'Values: {str(result)}'
        return message
    except Exception as error:
        print(error)
        return 'Error'

@app.route('/<key>/<value>')
def add_value(key, value):
    try:
        client.append(key, value)
        return f'Added {value} to {key}.'
    except Exception as error:
        print(error)
        return 'Error'

@app.route('/delete')
def delete():
    try:
        client.flushall()
        return f'Deleted'
    except Exception as error:
        print(error)
        return 'Error'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
