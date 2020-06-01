import datetime
import json
from decimal import Decimal

import pendulum


def json_dumps(obj):
    def to_json(python_object):
        if isinstance(python_object, (pendulum.Pendulum, datetime.datetime)):
            return python_object.timestamp()
        if isinstance(python_object, Decimal):
            return float(python_object)  # str(python_object).rstrip("0").rstrip(".")
        return str(python_object)

    return json.dumps(obj, default=to_json)
