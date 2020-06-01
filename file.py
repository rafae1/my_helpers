import os
import shutil


def make_empty_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
    os.mkdir(path)


def str_size_to_bytes(str_size):
    """
    :param str_size: str
    :return: int
    """
    multiplier_mapping = {
        "KB": 1024,
        "MB": 1024 ** 2,
        "GB": 1024 ** 3,
        "TB": 1024 ** 4,
        "PB": 1024 ** 5
    }

    postfix = str_size[-2:]

    multiplier = multiplier_mapping[
        postfix] if postfix in multiplier_mapping else 1
    base_size = int(''.join(filter(lambda c: c.isdigit(), str_size)))

    return base_size * multiplier
