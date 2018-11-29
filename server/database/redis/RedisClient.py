"""
A simple redis-cache interface for storing python objects.
"""
from binascii import crc32
import redis
import logging
import settings

DEFAULT_EXPIRY = 60 * 60 * 24



class RedisClient(object):

    def __init__(self, socket_connect_timeout=30, encoding='utf-8', socket_timeout=30, retry_on_timeout=True):
        # redis_nodes = [{'host': settings.REDIS_HOST, 'port': int(settings.REDIS_PORT)}]
        # server = StrictRedisCluster(host=settings.REDIS_HOST, port=int(settings.REDIS_PORT), startup_nodes=redis_nodes)
        pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=int(settings.REDIS_PORT))
        server = redis.Redis(connection_pool=pool)
        self.redis = server


    ### MRedis Specific Parts ###
    def get_node_offset(self, key):
        "Return the redis node list offset to use"

        raise self.redis

    def get_server_key(self, server):
        "Return a string of server:port:db"

        return "%s:%i:%i" % (server.host, server.port, server.db)

    #### SERVER INFORMATION ####
    def bgrewriteaof(self):
        """
        Run the bgrewriteoaf command for each server returning success indexed
        in a dictionary by server
        """

        response = {}

        key = self.get_server_key(self.redis)
        response[key] = self.redis.bgrewriteaof()
        return response

    def bgsave(self):
        """
        Run the bgsave command for each server returning success indexed in a
        dictionary by server
        """

        response = {}
        key = self.get_server_key(self.redis)
        response[key] = self.redis.bgsave()
        return response

    def dbsize(self):
        "Return the size of the database in a dictionary keyed by server"

        response = {}

        key = self.get_server_key(self.redis)
        response[key] = self.redis.dbsize()
        return response

    def flushall(self):
        """
        Flushes all databases for each redis server returning success indexed
        in a dictionary by server
        """

        response = {}

        key = self.get_server_key(self.redis)
        response[key] = self.redis.flushall()
        return response

    def flushdb(self):
        """
        Flushes the selected db for each redis server returning success indexed
        in a dictionary by server
        """

        response = {}
        key = self.get_server_key(self.redis)
        response[key] = self.redis.flushdb()
        return response

    def info(self):
        "Returns a dictionary keyed by Redis server of info command output"

        response = {}
        key = self.get_server_key(self.redis)
        response[key] = self.redis.info()
        return response

    def lastsave(self):
        "Returns a dictionary keyed by Redis server of lastsave command output"

        response = {}
        key = self.get_server_key(self.redis)
        response[key] = self.redis.lastsave()
        return response

    def ping(self):
        "Returns a dictionary keyed by Redis server of ping command output"

        response = {}
        key = self.get_server_key(self.redis)
        response[key] = self.redis.lastsave()
        return response

    def save(self):
        "Returns a dictionary keyed by Redis server of save command output"

        response = {}
        key = self.get_server_key(self.redis)
        response[key] = self.redis.save()
        return response

    ### Basic Key Commands
    def append(self, key, value):
        """
        Appends the string ``value`` to the value at ``key``. If ``key``
        doesn't already exist, create it with a value of ``value``.
        Returns the new length of the value at ``key``.
        """

        offset = self.get_node_offset(key)
        return self.redis.append(key, value)

    def decr(self, key, amount=1):
        """
        Decrements the value of ``key`` by ``amount``.  If no key exists,
        the value will be initialized as 0 - ``amount``
        """

        offset = self.get_node_offset(key)
        return self.redis.decr(key, amount)

    def delete(self, *key):
        "Delete one or more keys specified by ``key``"

        for temp in key:
            offset = self.get_node_offset(temp)
            if not self.redis.delete(temp):
                return False
        return True

    def exists(self, key):
        "Returns a boolean indicating whether ``key`` exists"

        offset = self.get_node_offset(key)
        return self.redis.exists(key)

    def expire(self, key, time):
        "Set an expire flag on ``key`` for ``time`` seconds"
        offset = self.get_node_offset(key)
        return self.redis.expire(key, time)

    def expireat(self, key, when):
        """
        Set an expire flag on ``key``. ``when`` can be represented
        as an integer indicating unix time or a Python datetime object.
        """

        offset = self.get_node_offset(key)
        return self.redis.expireat(key, when)

    def get(self, key):
        """
        Return the value at ``key``, or None of the key doesn't exist
        """

        offset = self.get_node_offset(key)
        return self.redis.get(key)

    def getset(self, key, value):
        """
        Set the value at ``key`` to ``value`` if key doesn't exist
        Return the value at key ``name`` atomically
        """

        offset = self.get_node_offset(key)
        return self.redis.getset(key, value)

    def incr(self, key, amount=1):
        """
        Increments the value of ``key`` by ``amount``.  If no key exists,
        the value will be initialized as ``amount``
        """

        offset = self.get_node_offset(key)
        return self.redis.incr(key, amount)

    def keys(self, pattern="*"):
        """
        Returns a list of keys matching ``pattern`` in a dictionary keyed by
        server
        """

        response = {}
        for server in self.servers:
            key = self.get_server_key(server)
            response[key] = server.keys(pattern)
        return response

    def mget(self):
        """
        Currently unimplemented due to complexity of perserving this behavior
        properly with multiple servers.
        """

        raise RedisClient.exceptions.UnextendedRedisCommand

    def move(self):
        """
        Currently unimplemented due to complexity of perserving this behavior
        properly with multiple servers.
        """

        raise RedisClient.exceptions.UnextendedRedisCommand

    def mset(self):
        """
        Currently unimplemented due to complexity of perserving this behavior
        properly with multiple servers.
        """

        raise RedisClient.exceptions.UnextendedRedisCommand

    def msetnx(self):
        """
        Currently unimplemented due to complexity of perserving this behavior
        properly with multiple servers.
        """

        raise RedisClient.exceptions.UnextendedRedisCommand

    def randomkey(self):
        "Returns the name of a random key from each server in a dictionary"

        response = {}

        key = self.get_server_key(self.redis)
        response[key] = self.redis.randomkey()
        return response

    def rename(self, key):
        """
        Currently unimplemented due to complexity of perserving this behavior
        properly with multiple servers.
        """

        raise RedisClient.exceptions.UnextendedRedisCommand

    def renamenx(self, key):
        """
        Currently unimplemented due to complexity of perserving this behavior
        properly with multiple servers.
        """

        raise RedisClient.exceptions.UnextendedRedisCommand

    def set(self, key, value):
        """
        Set the value at ``key`` to ``value``
        * The following flags have been deprecated *
        If ``preserve`` is True, set the value only if key doesn't already
        exist
        If ``getset`` is True, set the value only if key doesn't already exist
        and return the resulting value of key
        """
        return self.redis.set(key, value)

    def setex(self, key, value, time):
        """
        Set the value of ``key`` to ``value``
        that expires in ``time`` seconds
        """

        return self.redis.setex(key, value, time)

    def substr(self, key, start, end=-1):
        """
        Return a substring of the string at ``key``. ``start`` and ``end``
        are 0-based integers specifying the portion of the string to return.
        """
        return self.redis.substr(key, start, end)

    def ttl(self, key):
        "Returns the number of seconds until the ``key`` will expire"

        offset = self.get_node_offset(key)
        return self.servers[offset].ttl(key)

    def type(self, key):
        "Returns the type of ``key``"
        return self.redis.type(key)

    def watch(self, key):
        "Watches the value at ``key``, or None of the key doesn't exist"
        return self.redis.watch(key)

    def unwatch(self, key):
        "Unwatches the value at ``key``, or None of the key doesn't exist"
        return self.redis.unwatch(key)

    ### List Commands ###
    def blpop(self, keys, timeout=0):
        """
        Currently unimplemented due to complexity of perserving this behavior
        properly with multiple servers.
        """

        raise RedisClient.exceptions.UnextendedRedisCommand

    def brpop(self, keys, timeout=0):
        """
        Currently unimplemented due to complexity of perserving this behavior
        properly with multiple servers.
        """

        raise RedisClient.exceptions.UnextendedRedisCommand

    def lindex(self, key, index):

        return self.redis.lindex(key, index)

    def linsert(self, key, where, refvalue, value):

        return self.redis.linsert(key, where, refvalue, value)

    def llen(self, key):

        return self.redis.llen(key)

    def lpop(self, key):

        offset = self.get_node_offset(key)
        return self.servers[offset].lpop(key)

    def lpush(self, key, value):

        return self.redis.lpush(key, value)

    def lpushx(self, key, value):

        return self.redis.lpushx(key, value)

    def lrange(self, key, start, end):

        return self.redis.lrange(key, start, end)

    def lrem(self, key, value, num=0):

        return self.redis.lrem(key, value, num)

    def lset(self, key, index, value):

        return self.redis.set(key, index, value)

    def ltrim(self, key, start, end):

        return self.redis.ltrim(key, start, end)

    def rpop(self, key):

        return self.redis.rpop(key)

    def rpush(self, key, value):

        return self.redis.rpush(key, value)

    def rpushx(self, key, value):

        return self.redis.rpushx(key, value)

    def sort(self, key, start=None, num=None, by=None, get=None,
             desc=False, alpha=False, store=None):

        return self.redis.store(key, start, num, by, get, desc,
                                          alpha, None)

    #### SET COMMANDS ####
    def sadd(self, key, value):
        "Add ``value`` to set ``key``"

        return self.redis.sadd(key, value)

    def scard(self, key):
        "Return the number of elements in set ``key``"

        return self.redis.scard(key)

    def sdiff(self, keys, *args):
        """
        Currently unimplemented due to complexity of perserving this behavior
        properly with multiple servers.
        """

        raise RedisClient.exceptions.UnextendedRedisCommand

    def sdiffstore(self, dest, keys, *args):
        """
        Currently unimplemented due to complexity of perserving this behavior
        properly with multiple servers.
        """

        raise RedisClient.exceptions.UnextendedRedisCommand

    def sinter(self, keys, *args):
        """
        Currently unimplemented due to complexity of perserving this behavior
        properly with multiple servers.
        """

        raise RedisClient.exceptions.UnextendedRedisCommand

    def sinterstore(self, dest, keys, *args):
        """
        Currently unimplemented due to complexity of perserving this behavior
        properly with multiple servers.
        """

        raise RedisClient.exceptions.UnextendedRedisCommand

    def sismember(self, key, value):
        "Return a boolean indicating if ``value`` is a member of set ``key``"

        return self.redis.sismember(key, value)

    def smembers(self, key):
        "Return all members of the set ``key``"


        return self.redis.smembers(key)

    def smove(self, src, dst, value):
        """
        Currently unimplemented due to complexity of perserving this behavior
        properly with multiple servers.
        """

        raise RedisClient.exceptions.UnextendedRedisCommand

    def spop(self, key):
        "Remove and return a random member of set ``key``"

        return self.redis.spop(key)

    def srandmember(self, key):
        "Return a random member of set ``key``"

        return self.redis.srandmember(key)

    def srem(self, key, value):
        "Remove ``value`` from set ``key``"

        return self.redis.srem(key, value)

    def sunion(self, keys, *args):
        """
        Currently unimplemented due to complexity of perserving this behavior
        properly with multiple servers.
        """

        raise RedisClient.exceptions.UnextendedRedisCommand

    def sunionstore(self, dest, keys, *args):
        """
        Currently unimplemented due to complexity of perserving this behavior
        properly with multiple servers.
        """

        raise RedisClient.exceptions.UnextendedRedisCommand

    #### SORTED SET COMMANDS ####
    def zadd(self, key, value, score):
        "Add member ``value`` with score ``score`` to sorted set ``key``"

        return self.redis.zadd(key,score,value)

    def zcard(self, key):
        "Return the number of elements in the sorted set ``key``"
        return self.redis.zcard(key)

    def zcount(self, key, min, max):

        return self.redis.zcount(key, min, max)

    def zincrby(self, key, value, amount=1):
        "Increment the score of ``value`` in sorted set ``key`` by ``amount``"

        return self.redis.zadd(key, amount, value)

    def zinterstore(self, dest, keys, aggregate=None):
        """
        Currently unimplemented due to complexity of perserving this behavior
        properly with multiple servers.
        """

        raise RedisClient.exceptions.UnextendedRedisCommand

    def zrange(self, key, start, end, desc=False, withscores=False):
        """
        Return a range of values from sorted set ``key`` between
        ``start`` and ``end`` sorted in ascending order.
        ``start`` and ``end`` can be negative, indicating the end of the range.
        ``desc`` indicates to sort in descending order.
        ``withscores`` indicates to return the scores along with the values.
            The return type is a list of (value, score) pairs
        """

        return self.redis.zrange(key, start, end, desc, withscores)

    def zrangebyscore(self, key, min, max,
                      start=None, num=None, withscores=False):
        """
        Return a range of values from the sorted set ``key`` with scores
        between ``min`` and ``max``.
        If ``start`` and ``num`` are specified, then return a slice of the range.
        ``withscores`` indicates to return the scores along with the values.
            The return type is a list of (value, score) pairs
        """

        return self.redis.zrangebyscore(key, min, max, start, num,
                                                  withscores)

    def zrank(self, key, value):
        """
        Returns a 0-based value indicating the rank of ``value`` in sorted set
        ``key``
        """
        return self.redis.zrank(key, value)

    def zrem(self, key, value):
        "Remove member ``value`` from sorted set ``key``"

        return self.redis.zrem(key, value)

    def hmset(self,key,mapping):
        return self.redis.hmset(key,mapping)

    def hset(self,name,key,value):
        return self.redis.hset(name,key,value)

    def hget(self,name,key):
        return self.redis.hget(name,key)

    def hmget(self, name, keys):
        return self.redis.hmget(name,keys)
    
    def zremrangebyrank(self, key, min, max):
        """
        Remove all elements in the sorted set ``key`` with ranks between
        ``min`` and ``max``. Values are 0-based, ordered from smallest score
        to largest. Values can be negative indicating the highest scores.
        Returns the number of elements removed
        """
        return self.redis.zremrangebyrank(key, min, max)

    def zremrangebyscore(self, key, min, max):
        """
        Remove all elements in the sorted set ``key`` with scores
        between ``min`` and ``max``. Returns the number of elements removed.
        """

        return self.redis.zremrangebyscore(key, min, max)

    def zrevrange(self, key, start, num, withscores=False):
        """
        Return a range of values from sorted set ``key`` between
        ``start`` and ``num`` sorted in descending order.
        ``start`` and ``num`` can be negative, indicating the end of the range.
        ``withscores`` indicates to return the scores along with the values
            as a dictionary of value => score
        """

        return self.redis.zrevrange(key, start, num, withscores)

    def zrevrank(self, key, value):
        """
        Returns a 0-based value indicating the descending rank of
        ``value`` in sorted set ``key``
        """

        return self.redis.zrevrank(key, value)

    def zscore(self, key, value):
        "Return the score of element ``value`` in sorted set ``key``"

        return self.redis.zscore(key, value)

    def zunionstore(self, dest, keys, aggregate=None):
        """
        Currently unimplemented due to complexity of perserving this behavior
        properly with multiple servers.
        """

        raise RedisClient.exceptions.UnextendedRedisCommand

    def _zaggregate(self, command, dest, keys, aggregate=None):
        """
        Currently unimplemented due to complexity of perserving this behavior
        properly with multiple servers.
        """

        raise RedisClient.exceptions.UnextendedRedisCommand

    ### Pipeline Function ###
    def pipeline(self, key):

        return self.redis.pipeline()

class InvalidHashMethod(Exception):
    pass

_client = RedisClient()

def get_redis():
    return _client.redis