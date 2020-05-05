Running the benchmarks
======================

## About

This is an example task runner to test your redis cluster performance.

## How to

First, we will launch our task runner app which we will use to run our benchmarking tests.

```
## Check the current working directory and navigate into the `/benchmarks`
## directory if needed
$ cd ./benchmarks

## Create the "redis-benchmarks" task
$ cf push -f manifest.yml
```

After the `redis-benchmarks` task runner app has been deployed, we will need to
create the desired Redis services before running the benchmark tests using our task runner.

```
## Legacy Redis cluster
$ cf create-service redis32 standard-ha our-legacy-redis

## New AWS Redis cluster
$ cf create-service redis test-aws-redis our-aws-redis
```

Next, we will bind our Redis services to the task runner app `redis-benchmarks`.
*Note - When creating a Redis cluster, it may take a few minutes to deploy all of the nodes.*

```
## Bind the legacy Redis service
$ cf bind-service redis-benchmarks redis

## Bind the new AWS Redis service
$ cf bind-service redis-benchmarks redis32

## Restage the task runner to pick up the bound services
$ cf restage redis-benchmarks
```

Finally, we will run the benchmarking tasks.

```
## Testing the AWS Redis cluster
$  cf run-task redis-benchmarks "./run --service-name redis"

## Testing the K8 Redis cluster
$  cf run-task redis-benchmarks "./run --service-name redis32"

## View the logs of the benchmark results
$ cf logs --recent redis-benchmarks
```
