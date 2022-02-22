from __future__ import annotations
import asyncio
import logging
import aiofiles
import nest_asyncio
import uvloop
from aiohttp import request
from aiomultiprocess import Pool

from utils import BASE_HEADERS, set_logger

nest_asyncio.apply()  # jupyter
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
set_logger('myLogs.log')

async def get(u: str) -> None:
    try:
        async with request((method := 'GET'), u, headers=BASE_HEADERS) as r:
            logging.debug(f'{r.status} {method} {u}')
            if r.status == 200:
                filename = u.split('/')[-1]  # modify this as needed
                try:
                    async with aiofiles.open(filename, 'wb') as f:
                        await f.write(await r.read())
                except Exception as e:
                    logging.debug(f'Exception: {e} {u}')
            else:
                logging.debug(f'{r.status = } {u}')
    except Exception as e:
        logging.debug(f'Exception: {e} {u}')


async def main():
    urls = ['https://c8.alamy.com/comp/WWH9YM/siberia-husky-sled-dog-dogphoto-dog-photo-dog-photos-WWH9YM.jpg',
            'https://thumbs.dreamstime.com/b/french-bulldog-small-breed-domestic-dog-were-result-s-cross-ancestors-imported-england-local-136021670.jpg',
            'https://images.all-free-download.com/images/graphiclarge/cute_dog_photo_picture_7_168843.jpg']
    async with Pool(loop_initializer=uvloop.new_event_loop) as pool:
        await pool.map(get, urls)


if __name__ == '__main__':
    asyncio.run(main())
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
