from __future__ import annotations

import asyncio
import hashlib
import logging

import aiofiles
import uvloop
from aiohttp import request
from aiomultiprocess import Pool

from utils import set_logger, get_headers

HEADERS = get_headers('headers.txt')
set_logger('myLogs.log')


async def get(url: str) -> None:
    async with request(method := 'GET', url, headers=HEADERS) as r:
        logging.debug(f'{r.status} {method} {url}')
        if r.status in {200, 418}:
            try:
                fname = hashlib.md5(url.encode("utf-8")).hexdigest()
                async with aiofiles.open(fname, 'wb') as fw:
                    await fw.write(await r.read())
            except Exception as e:
                logging.debug(f'Exception: {e} {url}')


async def main():
    urls = ['https://c8.alamy.com/comp/WWH9YM/siberia-husky-sled-dog-dogphoto-dog-photo-dog-photos-WWH9YM.jpg',
            'https://thumbs.dreamstime.com/b/french-bulldog-small-breed-domestic-dog-were-result-s-cross-ancestors-imported-england-local-136021670.jpg',
            'https://images.all-free-download.com/images/graphiclarge/cute_dog_photo_picture_7_168843.jpg']

    async with Pool(loop_initializer=uvloop.new_event_loop) as pool:
        await pool.map(get, urls)


# todo cannot convert to notebook, must run this .py file
if __name__ == '__main__':
    asyncio.run(main())
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
