Node.js connection to AWS ElastiCache Redis
===========================================

An example app connecting to Redis using [ioredis](https://github.com/luin/ioredis)

## Migrating from your Redis service

The follow code snippet shows the differences between connecting to the old Redis service
to the new AWS ElastiCache Redis service. The following app code shows how to configure
the Redis client with the Redis service bound to the app. See this [ioredis issue](https://github.com/luin/ioredis/issues/1042#issuecomment-575642093) for more information.

```js
const Redis = require('ioredis');
const cfenv = require('cfenv');

//
// The old Redis service named `old-redis-service`
//
const redisConfig = appEnv.getService('old-redis-service');

const client = new Redis({
  host: redisConfig.credentials.hostname, // rename the credentials `hostname` to `host`
  port: redisConfig.credentials.port,
  password: redisConfig.credentials.password,
});


//
// The new AWS ElastiCache Redis service named `new-redis-service`
//
const redisConfig = appEnv.getService('new-redis-service');

const client = new Redis({
  host: redisConfig.credentials.host,
  port: redisConfig.credentials.port,
  password: redisConfig.credentials.password,
  tls: {}, // Set the tls key as an empty object
});


// The Redis `client` is ready to be used
```

## Differences in configuration

- The new AWS ElastiCache Redis service credentials has renamed the host name to `host` from `hostname`
- The `tls` configuration key must be set to an empty object `{}`
