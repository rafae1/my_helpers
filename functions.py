import asyncio
import functools


async def await_or_return(result_or_awaitable):
    if asyncio.iscoroutine(result_or_awaitable):
        return await result_or_awaitable
    return result_or_awaitable


async def wait_for(*iterable, timeout=10, exception_handler=lambda i, e: print()):
    return await asyncio.gather(
        *(_wait_one(coro, timeout, exception_handler, i) for i, coro in
          enumerate(iterable)))


async def _wait_one(coroutine, timeout, exception_handler, i):
    try:
        return await asyncio.wait_for(coroutine, timeout)
    except Exception as e:
        return exception_handler(i, e)


def retry(exception, tries=3, delay=3):
    """
    Decorator for repeated `tries` times in failure with `delay` seconds
    :param exception: Exception
    :param tries: int
    :param delay: int
    :return: decorator
    """

    def deco_retry(f):
        @functools.wraps(f)
        async def f_retry(*args, **kwargs):
            mtries = tries
            while mtries > 0:
                try:
                    return await f(*args, **kwargs)
                except exception as e:
                    print("{}, Retrying in {} seconds...".format(e, delay))
                    await asyncio.sleep(delay)
                    mtries -= 1
            return await f(*args, **kwargs)

        return f_retry

    return deco_retry
