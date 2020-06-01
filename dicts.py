import copy


def get_dicts_diff(old_dict, new_dict):
    old_dict = copy.copy(old_dict)
    new_dict = copy.copy(new_dict)

    ret = {}
    for k, old_val in old_dict.items():
        if new_dict.get(k) != old_val:
            ret[k] = [old_val, new_dict.pop(k, None)]

    for k, new_val in new_dict.items():
        if old_dict.get(k) != new_val:
            ret[k] = [old_dict.get(k, None), new_val]

    return ret
