from dataclasses import dataclass
import time

import redis


class RedisModel:
    HOST = "localhost"
    PORT = 6379
    DBID = 0
    REDIS_TIMEOUT = 3600 * 24 * 30


class Singleton(type):
    """
    An metaclass for singleton purpose. Every singleton class should inherit from this class by 'metaclass=Singleton'.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RedisPool(metaclass=Singleton):

    def __init__(self,
                 host: str = "localhost",
                 port: int = 6379,
                 db_id: int = 0) -> None:
        self.pool = redis.ConnectionPool(host=host, port=port, db=db_id)


@dataclass
class RedisDataModel(object):
    uid: str
    value: str
    checksum: str
    timestamp: int


class RedisCache(object):

    def __init__(self) -> None:
        pool = RedisPool(RedisModel.HOST, RedisModel.PORT,
                         RedisModel.DBID).pool
        self._conn = redis.StrictRedis(connection_pool=pool)

    def set(self, project: str, key: str, uid: str, value: str, checksum: str):
        name = f"{project}:{key}"

        if self._conn.exists(name):
            self._conn.delete(name)

        timestamp = int(time.time())
        self._conn.hset(name,
                        mapping={
                            "uid": uid,
                            "value": value,
                            "checksum": checksum,
                            "timestamp": timestamp
                        })

    def get(self, project: str, key: str):
        name = f"{project}:{key}"
        if not self._conn.exists(name):
            return None

        res = self._conn.hgetall(name)
        uid = res["uid".encode()].decode("utf-8")
        value = res["value".encode()].decode("utf-8")
        checksum = res["checksum".encode()].decode("utf-8")
        timestamp = res["timestamp".encode()].decode("utf-8")

        return RedisDataModel(uid, value, checksum, int(timestamp))


if __name__ == "__main__":
    handle = RedisCache()
    project = "test"
    key = "default"
    handle.set(project, key, uid="0", value="yuzuhakuon", checksum="name")

    res = handle.get(project, key)
    print(res)

    res = handle.get(project, "key")
    print(res)
