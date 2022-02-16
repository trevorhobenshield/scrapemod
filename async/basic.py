import asyncio
import logging
import os
import time
from enum import Enum
from pathlib import Path
from typing import Any, Optional

import aiohttp
import nest_asyncio
import uvloop
from bs4 import BeautifulSoup


class LogConstants(Enum):
    FMT = '%(asctime)s.%(msecs)03d %(levelname)s:\t%(message)s'
    DT_FMT = '%Y-%m-%d %H:%M:%S'
    DT_FMT_ALT = '%Y.%m.%dD%H:%M:%S'


if not os.path.exists('logs'):
    os.makedirs('logs')
logging.basicConfig(
    filename=f'logs/myLog.log',
    filemode='a',
    level=logging.DEBUG,
    format=LogConstants.FMT.value,
    datefmt=LogConstants.DT_FMT_ALT.value)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt=LogConstants.FMT.value,
                              datefmt=LogConstants.DT_FMT_ALT.value)
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

nest_asyncio.apply()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def save_html(data: list, filename: Optional[str] = None) -> None:
    out_path = Path('out')
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    name = f'{filename}-' if filename else ''
    for soup in data:
        with open(out_path / f"{name}{time.time_ns()}.html", 'w', encoding='utf-8') as fw:
            fw.write(soup.prettify())


def get_headers(fname: str) -> dict:
    return {t[0].lower(): t[-1].strip()
            for t in (s.partition(':')
                      for s in Path(fname).read_text().split('\n') if s)}


async def get(url: str, session: aiohttp.ClientSession) -> Any:
    try:
        logging.debug(f"Downloading: {url}")
        response = await session.request(method='get', url=url)
        data = await response.text()
        soup = BeautifulSoup(data, 'html.parser')
        return soup
    except Exception as e:
        print(e)


async def process_requests(urls: list) -> list:
    async with aiohttp.ClientSession(headers=get_headers('headers.txt')) as s:
        return await asyncio.gather(*(get(u, s) for u in urls))


def main():
    urls = Path('urls.txt').read_text().splitlines()
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(process_requests(urls))
    save_html(res)


if __name__ == '__main__':
    main()
