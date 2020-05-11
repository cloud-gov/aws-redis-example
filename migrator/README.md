Migrating Cloud.gov legacy Redis to AWS ElastiCache Redis
=========================================================

An example task runner for migrating from the legacy `redis32` service to the new
`redis` service using AWS ElastiCache.

## How to

### Deploying the migration task

First, we will launch our task runner app which we will use to migrate our Redis services.

```
## Check the current working directory and navigate into the `/migrator`
## directory if needed
$ cd ./migrator

## Create the "redis-migrator" task
$ cf push -f manifest.yml
```

### Binding the Redis services

Next, we will bind our Redis services to the task runner app `redis-migrator`.
*Note - When creating a Redis cluster, it may take a few minutes to deploy all of the nodes.*

```
## Bind the source Redis service
$ cf bind-service redis-migrator <source redis service name>

## Bind the destination Redis service
$ cf bind-service redis-migrator <destination redis service name>

## Restage the task runner to pick up the bound services
$ cf restage redis-migrator
```

### Running the migration

We can kick off a task to migrate keys from the the Redis

```
# Run the migration task

$ cf run-task redis-migrator \
  "./run migrate --src <source redis service name> --dest <destination redis service name>"

## Additional available migration flags that can be added to the above task migration command
##
  -s, --src <source redis service name>
        Required
        The CF name of the source Redis service

  -d, --dest <destination redis service name>
        Required
        The CF name of the destination Redis service

  -f, --flush
        Default: False
        Flush all keys from the destination Redis

  -rdk, --replace-destination-keys
        Default: True
        Replaces duplicate keys on destination Redis with source Redis keys/values
##
```

### Removing the migration task

After migration is complete, you can remove the task runner from you space.

```
  cf delete redis-migrator
```
