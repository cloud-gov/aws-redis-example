const express = require('express');
const Redis = require('ioredis');
const cfenv = require('cfenv');
const appEnv = cfenv.getAppEnv();
const app = express();

const port = process.env.PORT || 3000;

const redisConfig = appEnv.getService('redis-aws-ha');

const client = new Redis({
  host: redisConfig.credentials.host,
  port: redisConfig.credentials.port,
  password: redisConfig.credentials.password,
  tls: {},
});

app.get('/', (req, res) => {
  return client.keys("*")
    .then(result => {
      res.send(`Keys: ${result}`)
    })
    .catch(error => {
      console.log(error)
      res.send('Error')
    });
});

app.get('/:key', (req, res) => {
  const key = req.params.key;
  return client.get(key)
    .then(result => {
      res.send(`Key ${key}: ${result}`)
    })
    .catch(error => {
      console.log(error)
      res.send('Error')
    });
});

app.post('/:key/:value', (req, res) => {
  const { key, value } = req.params;
  return client.set(key, value)
    .then(result => {
      console.log(result);
      res.send(`Key ${key} set value ${value}`);
    })
    .catch(error => {
      console.log(error)
      res.send('Error')
    });
});

app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`));
