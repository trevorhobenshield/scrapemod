from __future__ import annotations

import asyncio
import logging
from pathlib import Path

import nest_asyncio
import uvloop
from aiohttp import request
from aiomultiprocess import Pool
from bs4 import BeautifulSoup

from utils import BASE_HEADERS, save_html, set_logger

nest_asyncio.apply()  # jupyter
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
set_logger('myLogs.log')


async def get(u: str) -> None:
    """
    save data on the fly
    """
    try:
        async with request((method := 'GET'), u, headers=BASE_HEADERS) as r:
            logging.debug(f'{r.status} {method} {u}')
            if r.status == 200:
                try:
                    save_html(BeautifulSoup(await r.text("utf-8"), 'html.parser'))
                except Exception as e:
                    logging.debug(f'Exception: {e} {u}')
            else:
                logging.debug(f'{r.status = } {u}')
    except Exception as e:
        logging.debug(f'Exception: {e} {u}')


async def main():
    urls = Path('urls.txt').read_text().splitlines()

    async with Pool(loop_initializer=uvloop.new_event_loop) as pool:
        await pool.map(get, urls)


if __name__ == '__main__':
    asyncio.run(main())
