import random
import secrets
import string


def random_string(chars=string.ascii_lowercase + string.digits, size=None):
    if not size:
        size = random.randrange(15, 25)
    return ''.join(secrets.choice(chars) for i in range(size))


def random_digit_string(size=None):
    return random_string(chars=string.digits, size=size)
