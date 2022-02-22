from __future__ import annotations

import asyncio
import logging
import os
import time
from enum import Enum
from pathlib import Path
import nest_asyncio
import uvloop
from aiohttp import request
from aiomultiprocess import Pool
from bs4 import BeautifulSoup
from icecream import ic
from utils import BASE_HEADERS

ic.configureOutput(includeContext=True)
nest_asyncio.apply()  # jupyter
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

HEADERS = BASE_HEADERS  # randomly init user-agent once

class LogConstants(Enum):
    FILENAME = 'MyLogs.log'
    FMT = '%(asctime)s.%(msecs)03d %(levelname)s:\t%(message)s'
    DT_FMT = '%Y-%m-%d %H:%M:%S'
    DT_FMT_ALT = '%Y.%m.%dD%H:%M:%S'


class Dirs(Enum):
    DATA = Path('data')
    LOGS = Path('logs')


os.makedirs(Dirs.DATA.value) if not os.path.exists(Dirs.DATA.value) else ...
os.makedirs(Dirs.LOGS.value) if not os.path.exists(Dirs.LOGS.value) else ...
logging.basicConfig(
    filename=Dirs.LOGS.value / LogConstants.FILENAME.value,
    filemode='a',
    level=logging.DEBUG,
    format=LogConstants.FMT.value,
    datefmt=LogConstants.DT_FMT_ALT.value
)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    fmt=LogConstants.FMT.value,
    datefmt=LogConstants.DT_FMT_ALT.value
)
console.setFormatter(formatter)
logging.getLogger().addHandler(console)


async def get(u: str) -> None:
    """
    save data on the fly
    """
    try:
        async with request((method := 'GET'), u, headers=HEADERS) as r:
            logging.debug(f'{r.status} {method} {u}')
            if r.status == 200:
                try:
                    with open(Dirs.DATA.value / f"{time.time_ns()}.html", 'w', encoding='utf-8') as fw:
                        fw.write(BeautifulSoup(await r.text("utf-8"), 'html.parser').prettify())
                except Exception as e:
                    logging.debug(f'Exception: {e} {u}')
            else:
                logging.debug(f'{r.status = } {u}')
    except Exception as e:
        logging.debug(f'Exception: {e} {u}')


async def main():
    urls = [
        'https://seattle.craigslist.org/search/cto?query=mercedes',
        'https://seattle.craigslist.org/search/cto?s=120&query=mercedes',
        'https://seattle.craigslist.org/search/cto?query=bmw',
        'https://seattle.craigslist.org/search/cto?s=120&query=bmw',
        'https://seattle.craigslist.org/search/cto?query=audi',
        'https://seattle.craigslist.org/search/cto?s=120&query=audi',
    ]

    async with Pool(loop_initializer=uvloop.new_event_loop) as pool:
        await pool.map(get, urls)


if __name__ == '__main__':
    asyncio.run(main())
