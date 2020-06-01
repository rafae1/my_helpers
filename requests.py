import asyncio
import traceback
from collections import namedtuple

import aiohttp

HttpResponse = namedtuple('HttpResponse', ['status', 'content', 'exception'])


async def request_multi(common_data, data, method="GET", loop=None):
    """ если есть одинаковые данные (например timeout),
    то их можно один раз задать в common_data,
    различающиеся(например url) надо задавать в data """

    async with aiohttp.ClientSession(loop=loop) as session:

        method = method.lower()
        method = getattr(session, method)

        async def send_postback(data):
            try:
                async with method(**common_data, **data) as resp:
                    content = await resp.read()
                    try:
                        content = content.decode()
                    except Exception:
                        content = str(content)
                    return HttpResponse(resp.status, content, None)
            except Exception:
                return HttpResponse(-1, "", traceback.format_exc())

        ret = await asyncio.gather(*[send_postback(d) for d in data], loop=None, return_exceptions=True)
        for i, r in enumerate(ret):
            if isinstance(r, Exception):
                ret[i] = HttpResponse(-1, "", r)
        return ret


async def request_multi_ex(data, common_data=None, loop=None):
    """ универсальный метод, как и для POST запросов, так и для GET """
    if not common_data:
        common_data = {}

    async with aiohttp.ClientSession(loop=loop) as session:

        async def send_postback(_data):
            try:
                async with session.request(*_data['args'], **_data['kwargs'],
                                           **common_data) as resp:
                    return HttpResponse(resp.status, await resp.text(), None)
            except Exception:
                return HttpResponse(-1, "", traceback.format_exc())

        ret = await asyncio.gather(*[send_postback(d) for d in data], loop=None, return_exceptions=True)
        for i, r in enumerate(ret):
            if isinstance(r, Exception):
                ret[i] = HttpResponse(-1, "", r)
        return ret
