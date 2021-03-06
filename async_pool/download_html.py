from __future__ import annotations

import asyncio
import logging
from pathlib import Path

import uvloop
from aiohttp import request
from aiomultiprocess import Pool
from bs4 import BeautifulSoup

from utils import save_soup, set_logger, get_headers, tag_soup

set_logger('downloaded_html.log')
HEADERS = get_headers('headers.txt')


async def get(url: str) -> None:
    async with request(method := 'GET', url, headers=HEADERS) as r:
        logging.debug(f'{r.status} {method} {url}')
        if r.status in {200, 418}:
            try:
                dat = await r.text("utf-8")
                soup = tag_soup(BeautifulSoup(dat), url)
                save_soup(soup)
            except Exception as e:
                logging.debug(f'Exception: {e} {url}')


async def main():
    urls = Path('urls.txt').read_text().splitlines()
    async with Pool(loop_initializer=uvloop.new_event_loop) as pool:
        await pool.map(get, urls)


# todo cannot convert to notebook, must run this .py file
if __name__ == '__main__':
    asyncio.run(main())
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
