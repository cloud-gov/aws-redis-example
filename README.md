# aws-redis-example [Work In Progress]

## About

This repository has a series of examples for migrating your cloud.gov applications
from using the `redis32` service running on the `standard-ha`, `standard`, and `micro` plans to the
`redis` service running on the `redis-5node`, `redis-3node`, and `redis-single` plans powered by
[AWS ElastiCache Redis](https://aws.amazon.com/elasticache/redis/). 

## Examples

The following is a list of different language examples for connecting and using the updated Redis service
offering which leverages AWS ElastiCache Redis.

- [Python](./python/README.md)
- [Nodejs](./node/README.md)
- More to come...

## Additional AWS ElastiCache Redis resources

- [What Is Amazon ElastiCache for Redis](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/WhatIs.html)
- The new service broker will create new Redis clusters with
  [at-rest encryption](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/at-rest-encryption.html) and
  [in-Transit encryption](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/in-transit-encryption.html)
- The cloud.gov [aws-broker](https://github.com/cloud-gov/aws-broker) provides the underlying marketplace service

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for additional information.

## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
