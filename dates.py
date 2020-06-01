import datetime
from numbers import Number

import pendulum
import pytz

DEFAULT_TZ_NAME = "Europe/Moscow"


def now():
    return pendulum.now(tz=DEFAULT_TZ_NAME)


def tomorrow():
    return pendulum.Pendulum.tomorrow(tz=DEFAULT_TZ_NAME)


def get_yesterday():
    return pendulum.Pendulum.yesterday(tz=DEFAULT_TZ_NAME)


def get_datetime(date, tz_name=None, *args):
    tz = pytz.timezone(tz_name or DEFAULT_TZ_NAME)
    if isinstance(date, int):
        return pendulum.Pendulum(date, *args, tzinfo=tz)
    if isinstance(date, datetime.datetime):
        return pendulum.Pendulum.instance(date, tz).astimezone(tz)
    if isinstance(date, str):
        return parse_date(date)
    return pendulum.Pendulum.instance(
        datetime.datetime.combine(date, datetime.time.min), tz).astimezone(tz)


def to_timestamp(dt):
    return dt.timestamp()


def from_timestamp(dt):
    return pendulum.fromtimestamp(dt, tz=DEFAULT_TZ_NAME)


def parse_date(date_string, tz=None):
    if isinstance(date_string, Number):
        return from_timestamp(date_string)
    if date_string.replace(".", "", 1).isdigit():
        return from_timestamp(float(date_string))
    return pendulum.parse(date_string,
                          tz=tz if tz is not None else DEFAULT_TZ_NAME).astimezone(
        DEFAULT_TZ_NAME)


def _period_index(_val):
    if _val == 1:
        return 0
    elif _val in (2, 3, 4):
        return 1
    else:
        return 2


TRANSLATIONS = {
    'ru': {
        'day': (("день", "день"), "дня", "дней"),
        'hour': (("час", "час"), "часа", "часов"),
        'minute': (("минута", "минуту"), "минуты", "минут"),
        'second': (("секунда", "секунду"), "секунды", "секунд"),
    },
    'en': {
        'day': (("day", "day"), "days", "days"),
        'hour': (("hour", "hour"), "hours", "hours"),
        'minute': (("minute", "minute"), "minutes", "minutes"),
        'second': (("second", "second"), "seconds", "seconds"),
    }
}


def get_humanize_seconds(seconds: int, at=False, extension=False,
                         language='ru'):
    """
        возвращает строковое представление количества секунд
        если нужны минуты умножь исходное на 60 и т.д.
        at = False (результат: 31мин - 31 минута)
        at = True (результат: 31мин - 31 минуту (например за 31 минуту))
        extension = False (результат: ровно 24часа = 24часа)
        extension = True (результат: ровно 24часа = 1 день) - укрупнение периода
    """

    result = []
    seconds_list = (
        (60 * 60 * 24, TRANSLATIONS[language]['day']),
        (60 * 60, TRANSLATIONS[language]['hour']),
        (60, TRANSLATIONS[language]['minute']),
        (0, TRANSLATIONS[language]['second']),
    )

    val = abs(seconds)
    for num, texts in seconds_list:
        if not val:
            continue
        if val < num:
            continue
        if val == num and not extension:
            continue

        if not num:
            d = val
            val = 0
        else:
            d = val // num
            val -= (d * num)
        index = _period_index(d % 10 if d > 20 else d)
        humanize = texts[index][at] if index == 0 else texts[index]
        result.append("%s %s" % (d, humanize))
    result_str = ', '.join(result) or "0 секунд"
    return ("-" if seconds < 0 else "") + result_str
