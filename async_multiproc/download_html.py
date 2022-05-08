from __future__ import annotations

import asyncio
import logging
from pathlib import Path

import uvloop
from aiohttp import request
from aiomultiprocess import Pool
from bs4 import BeautifulSoup

from utils import save_html, set_logger, get_headers

set_logger('downloaded_html.log')
HEADERS = get_headers('headers.txt')


async def get(u: str) -> None:
    try:
        async with request(method := 'GET', u, headers=HEADERS) as r:
            logging.debug(f'{r.status} {method} {u}')
            if r.status == 200:
                try:
                    data = await r.text("utf-8")
                    soup = BeautifulSoup(data, 'html.parser')
                    p = soup.new_tag('p', id='scrape_url')
                    p.string = u
                    soup.html.body.insert(0, p)
                    save_html(soup)
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
