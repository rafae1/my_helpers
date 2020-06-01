from itertools import islice
from typing import List


def get_unique_list(lst):
    """ уникальный список (без повторений) с сохранением порядка """
    ret = []
    added = set()
    for el in lst:
        if el not in added:
            ret.append(el)
            added.add(el)
    return ret


def is_all_unique(iterable):
    seen = set()
    for elem in iterable:
        before = len(seen)
        seen.add(elem)
        if before == len(seen):
            return False
    return True


def get_doubled(lst):
    return set([x for x in lst if lst.count(x) > 1])


def cleanup_lists(main: List, *additional: List, key=lambda x: x):
    keys_to_remove = [i for i, v in enumerate(main) if key(v)]

    for i in reversed(keys_to_remove):
        for lst in (main, *additional):
            lst.pop(i)


def chunked(arr, n):
    arr = iter(arr)
    chunk = list(islice(arr, n))
    while chunk:
        yield chunk
        chunk = list(islice(arr, n))
