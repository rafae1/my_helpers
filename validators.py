import re
from .exceptions import ValidateException


EMAIL_REGEXP = r"^[a-zA-Z0-9.!#$%&'*+/\\\[\]@=?^_`{|}~-]+@[A-z0-9.-]+\.[A-z]{2,}$"

# https://github.com/guyhughes/fqdn/blob/develop/fqdn/__init__.py#L28
HOSTNAME_REGEXP = re.compile(r'^((?!-)[-A-Z\d]{1,62}(?<!-)\.)+[A-Z]{1,62}\.?$',
                             re.IGNORECASE)

CLEAR_STRING_REGEXP = re.compile(r'[\x00-\x1f]')


def get_email(email):
    try:
        email = get_str(255)(email)
        res = re.match(EMAIL_REGEXP, email, re.I)
        return res.group().lower()
    except AttributeError:
        raise ValidateException("Wrong email")


def get_int_arr(str_or_list):
    try:
        return list(map(int, filter(None, str_or_list.split(',') if isinstance(
            str_or_list, str) else str_or_list)))
    except TypeError:
        raise ValidateException('should be list of integers')


def get_float(string):
    try:
        return float(string)
    except TypeError:
        raise ValidateException('should be float')


def get_int(string):
    try:
        return int(string)
    except TypeError:
        raise ValidateException('should be integer')


def get_str(string_or_length=None, clear=False):
    if isinstance(string_or_length, str):
        value = string_or_length
        return value.strip()
    else:
        def check_str(value):
            max_length = string_or_length
            value = value.strip()
            if clear:
                value = CLEAR_STRING_REGEXP.sub("", value)
            if max_length and len(value) > max_length:
                raise ValidateException("invalid string length")
            return value

        return check_str


def get_arr(arr_str_or_type):
    get_list = lambda x: (
        list(filter(None, x.split(',')) if isinstance(x, str) else x))
    try_strip = lambda x: x.strip() if isinstance(x, str) else x
    # если вызвана как просто функция
    if isinstance(arr_str_or_type, str):
        return [try_strip(s) for s in get_list(arr_str_or_type)]
    # если вызвана как фабрика функций
    else:
        _type = arr_str_or_type
        return lambda arr_str: [_type(try_strip(s)) for s in get_list(arr_str)]


def validate_number(regex, number, error_msg):
    if not number:
        return
    if number:
        res = re.search(regex, number, re.I)
        if not res:
            raise ValidateException(error_msg)
        return res.group(1)


def get_phone(phone_num):
    return validate_number("(^[\d\+\-\s]{6,20}$)", phone_num, 'wrong phone number')


def get_skype(skype):
    return validate_number("(^[a-zA-Z0-9\\.,\-\_\@]{6,32}$)", skype, 'wrong skype')


def get_telegram(telegram):
    return validate_number("(^[a-zA-Z0-9\/\\\+.,\:\-\_\@]{5,50}$)", telegram, 'wrong telegram')


def get_wmr(wmr):
    return validate_number("(^(R)[0-9]{12}$)", wmr, 'wrong wallet number')


def get_bool(value):
    u"""
    Проверка и парсинг принятых в текстовом формате с клиента булевских
    значений (чекбоксы и так далее)
    """
    assert value in [True, False, None, "true", "false", "undefined"]

    if value == "true":
        value = True
    elif value == "false" or value == "undefined":
        value = False

    return value


def get_url(url):
    if not str(url).startswith('http'):
        url = 'http://%s' % url
    if len(url) > 255:
        raise ValidateException('invalid url')

    regex = re.compile(
        u"^"
        u"(?:(?:https?)://)"
        u"(?:"
        # host name
        u"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
        # domain name
        u"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
        # TLD identifier
        u"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
        u")"
        # port number
        u"(?::\d{2,5})?"
        # query string
        u"(?:\/?\S*)?"
        # fragment
        u"(?:#\S*)?"
        u"$",
        re.UNICODE | re.IGNORECASE)
    if not regex.search(url):
        raise ValidateException('invalid url')
    return url


def get_hostname(hostname: str):
    hostname = hostname[:-1] if hostname.endswith('.') else hostname
    for protocol in ['https://', 'http://']:
        hostname = hostname.replace(protocol, '', 1) if hostname.startswith(
            protocol) else hostname

    if len(hostname) > 253:
        raise ValidateException('invalid domain')

    if HOSTNAME_REGEXP.match(hostname):
        return hostname.lower()
    else:
        raise ValidateException('invalid domain')
