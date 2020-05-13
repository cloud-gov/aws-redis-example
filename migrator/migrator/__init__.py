import os
from cfenv import AppEnv
import redis


def redis_client(service_name):
    """
        Connecting to a Redis service
    """
    config = dict(host=service_name, port=6379, password="", ssl_cert_reqs=None)

    if service_name is None:
        return None

    try:
        if "VCAP_SERVICES" in os.environ:
            env = AppEnv()
            service = env.get_service(name=service_name)
            credentials = service.credentials

            if credentials.get("hostname"):
                config["host"] = credentials["hostname"]
            else:
                config["host"] = credentials["host"]
                config["ssl"] = True

            config["port"] = int(credentials["port"])
            config["password"] = credentials["password"]

        client = redis.Redis(**config)
    except redis.ConnectionError:
        client = None

    return client


class Migrator:
    """
        This is the Migrator class to connect and run migrations between redis services.
    """

    def __init__(
        self, src_service_name, dest_service_name, flush=False, replace_dest_keys=True
    ):
        self.src_client = redis_client(src_service_name)
        self.dest_client = redis_client(dest_service_name)
        self.flush = flush
        self.replace_dest_keys = replace_dest_keys

    def copy_keys(self, keys, src_pipeline, missing_keys, existing_keys):
        """
            Method to copy keys from source to destination Redis
        """

        src_result = src_pipeline.execute()

        dst_pipe = self.dest_client.pipeline()

        for key, ttl, data in zip(keys, src_result[::2], src_result[1::2]):
            if data != None:
                dst_pipe.restore(
                    key, ttl if ttl > 0 else 0, data, replace=self.replace_dest_keys
                )
            else:
                missing_keys += 1

        dst_result = dst_pipe.execute(False)

        for key, result in zip(keys, dst_result):
            if result != b"OK":
                e = result
                if hasattr(e, "args") and e.args[0] in (
                    "BUSYKEY Target key name already exists.",
                    "Target key name is busy.",
                ):
                    existing_keys += 1
                else:
                    print("Key failed:", key, repr(data), repr(result))
                    raise e

        return missing_keys, existing_keys

    def run_migration(self, pattern="*", BATCH_SIZE=100):
        """
            Method to run migration from source to destination Redis
        """
        num_keys = 0

        try:
            if self.flush:
                print("Flushing destination Redis keys.")
                self.dest_client.flushall()

            dbs = self.src_client.info("keyspace")

            for db in dbs:
                num_keys += int(dbs[db]["keys"])

            if num_keys == 0:
                print("No keys found, exiting.")
                return

            cursor = 0
            missing_keys = 0
            existing_keys = 0

            keys = []
            src_pipeline = self.src_client.pipeline()

            for key in self.src_client.scan_iter(match=pattern):
                cursor += 1
                keys.append(key)
                src_pipeline.pttl(key)
                src_pipeline.dump(key)

                if cursor % BATCH_SIZE == 0:

                    missing_keys, existing_keys = self.copy_keys(
                        keys, src_pipeline, missing_keys, existing_keys
                    )

                    keys = []
                    src_pipeline = self.src_client.pipeline()

            missing_keys, existing_keys = self.copy_keys(
                keys, src_pipeline, missing_keys, existing_keys
            )

            print(f"Number of keys missing on source Redis during scan: {missing_keys}")
            print(
                f"Number of keys already existing on destination Redis: {existing_keys}"
            )

            dest_dbs = self.dest_client.info("keyspace")
            dest_num_keys = 0

            for db in dest_dbs:
                dest_num_keys += int(dest_dbs[db]["keys"])

            print(f"Keys migrated: {dest_num_keys}")

        except Exception as e:
            print(e)

    def seed_source(self, records_per_seed=5000):
        """
            Method to seed the source client with data for testing
        """
        for x in range(records_per_seed):
            self.src_client.set(f"key-{x}", f"value={x}")

        for x in range(records_per_seed):
            self.src_client.set(f"key-num-{x}", x * 2)

        for x in range(records_per_seed):
            key = f"key-ttl-{x}"
            self.src_client.set(key, f"value-with-ttl={x}")
            self.src_client.expire(key, 1000)

        for x in range(records_per_seed):
            key = f"key-num-ttl-{x}"
            self.src_client.set(key, x * 2)
            self.src_client.expire(key, 1000)

    def flush_source(self):
        self.src_client.flushall()


__version__ = "0.0.1"


__all__ = [Migrator]
