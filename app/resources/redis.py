import json
from datetime import datetime
from logging import Logger
from typing import Any, Optional
import collections

import redis

import config

# logger: Logger = DevOpsLogger.get_logger(__name__)

ISSUE_FAMILIES_KEY = "issue_families"
PROJECT_ISSUE_CALCULATE_KEY = "project_issue_calculation"


class RedisOperator:
    def __init__(self):
        self.redis_base_url = config.get("REDIS_BASE_URL")
        # prod
        self.pool = redis.ConnectionPool(
            host=self.redis_base_url.split(":")[0],
            port=int(self.redis_base_url.split(":")[1]),
            decode_responses=True,
        )
        self.r = redis.Redis(connection_pool=self.pool)

    #####################
    # String type
    #####################
    def str_get(self, key):
        return self.r.get(key)

    def str_set(self, key, value):
        return self.r.set(key, value)

    def str_delete(self, key):
        self.r.delete(key)

    #####################
    # Boolean type
    #####################
    def bool_get(self, key: str) -> bool:
        """
        Get a boolean value from redis. Redis stores boolean into strings,
        so this function will convert strings below to ``True``.

            - "1"
            - "true"
            - "yes"

        Other values will be converted to ``False``.

        :param key: The key to get
        :return: The result from redis server
        """
        value: Optional[str] = self.r.get(key)
        if value:  # if value is not None or not empty string
            if value.lower() in ("1", "true", "yes"):
                return True
        return False

    def bool_set(self, key: str, value: bool) -> bool:
        """
        Set a boolean value to redis.

        :param key: The key to set
        :param value: The boolean value to set
        :return: True if set successfully, False if not
        """
        return self.r.set(key, str(value).lower())

    def bool_delete(self, key: str) -> bool:
        """
        Delete a key from redis.

        :param key: The key to delete
        :return: True if the key was deleted, False if the key did not exist
        """
        result: int = self.r.delete(key)
        if result == 1:
            return True
        else:
            return False

    #####################
    # Dictionary type
    #####################
    def dict_set_all(self, key, value):
        return self.r.hset(key, mapping=value)

    def dict_set_certain(self, key, sub_key, value):
        return self.r.hset(key, sub_key, value)

    def dict_calculate_certain(self, key, sub_key, num=1):
        return self.r.hincrby(key, sub_key, amount=num)

    def dict_get_all(self, key):
        return self.r.hgetall(key)

    def dict_get_certain(self, key, sub_key):
        return self.r.hget(key, sub_key)

    def dict_delete_certain(self, key, sub_key):
        return self.r.hdel(key, sub_key)

    def dict_delete_all(self, key):
        value = self.r.hgetall(key)
        self.r.delete(key)
        return value

    def list_keys(self, pattern):
        return [key for key in self.r.scan_iter(pattern)]

    def dict_len(self, key):
        return self.r.hlen(key)


redis_op = RedisOperator()
