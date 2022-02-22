import asyncio
import logging
from pathlib import Path

import aiohttp
import nest_asyncio
import uvloop
from bs4 import BeautifulSoup

from utils import set_logger, BASE_HEADERS, save_html

nest_asyncio.apply()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def get(url: str, session: aiohttp.ClientSession) -> BeautifulSoup:
    try:
        logging.debug(f"Downloading: {url}")
        response = await session.request(method='GET', url=url)
        data = await response.text()
        return BeautifulSoup(data, 'html.parser')
    except Exception as e:
        print(e)


async def process_requests(urls: list, headers: dict) -> list:
    async with aiohttp.ClientSession(headers=headers) as s:
        return await asyncio.gather(*(get(u, s) for u in urls))


def main():
    set_logger('myLog.log')
    urls = Path('urls.txt').read_text().splitlines()
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(process_requests(urls, BASE_HEADERS))
    [save_html(r) for r in res]


if __name__ == '__main__':
    main()
