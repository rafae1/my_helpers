from itertools import islice

import math

max_int32 = 2147483647
min_int32 = -2147483648
max_uint32 = 4294967295


def chunked(arr, n):
    arr = iter(arr)
    chunk = list(islice(arr, n))
    while chunk:
        yield chunk
        chunk = list(islice(arr, n))


def truncate(value, min_val, max_val):
    if not value:
        return value
    if value > max_val:
        return max_val
    if value < min_val:
        return min_val
    return value


def truncate_int32(value):
    return truncate(value, min_int32, max_int32)


def truncate_uint32(value):
    return truncate(value, 0, max_uint32)


def make_number(val):
    """ заменяем бесконечности и NaN на 0 """
    return 0 if isinstance(val, float) and (
            val in [float('inf'), float('-inf')] or math.isnan(val)) \
        else val


def format_num(num, decimal_places=2, group_delimiter=' ',
               decimal_delimiter=','):
    if decimal_places:
        x, y = (f"%.{decimal_places}f" % num).split(".")
        y = decimal_delimiter + y
    else:
        x, y = "%d" % num, ''
    return group_delimiter.join([''.join(d3) for d3 in chunked(x[::-1], 3)])[
           ::-1] + y
