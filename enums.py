from enum import IntEnum
from functools import lru_cache

from .classes import classproperty


class BaseIntEnum(IntEnum):
    __labels__ = None

    @classproperty
    def default(cls):
        return list(cls.__members__.values())[0]

    @classmethod
    @lru_cache()
    def codes_by_val(cls):
        return {v: k for (k, v) in cls.__members__.items()}

    @classmethod
    def items(cls):
        return [{
            "value": v,
            "name": k.lower(),
            "label": cls.verbose(v, default=k)
        } for k, v in cls.__members__.items()]

    @classmethod
    def verbose(cls, key=None, default=''):
        if key is None:
            return cls.__labels__ or {}
        return (cls.__labels__ or {}).get(key,
                                          cls.codes_by_val().get(key, default))

    @classmethod
    def is_available(cls, value):
        return value in [v.value for _, v in cls.__members__.items()]

    @classmethod
    def choices(cls):
        return tuple((int(v), k) for k, v in cls.__members__.items())

    @classmethod
    def options(cls):
        return [{"value": v, "label": cls.verbose(v)} for k, v in
                cls.__members__.items()]

    @classmethod
    def code(cls, val):
        return cls.codes_by_val()[val]

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

    def __str__(self):
        return "%s" % self.value

    def __repr__(self):
        return "%s" % self.value
