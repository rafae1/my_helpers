def to_camel_case(string):
    return ''.join(x.title() for x in string.split('_'))


def to_snake_case(string):
    return "".join([f"_{chr(ord(x) + 32)}" if 65 <= ord(x) <= 90 else x for x in
                    string]).lstrip("_")


def masking(string, symbol='*', amount=2):
    if not string:
        return string
    amount = min(amount, len(string))
    return string[:-amount] + symbol * amount
