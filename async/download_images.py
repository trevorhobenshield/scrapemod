import asyncio
import hashlib
import logging

import aiofiles
import aiohttp
import nest_asyncio
import uvloop

from utils import set_logger, get_headers

nest_asyncio.apply()  # needed if running in notebook
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())  # modified event loop


async def download_image(url: str, session: aiohttp.ClientSession):
    try:
        logging.debug(f"Downloading: {url}")
        res = await session.request(method='GET', url=url)
        dat = await res.read()
        unique_filename = hashlib.md5(url.encode("utf-8")).hexdigest()
        async with aiofiles.open(f'{unique_filename}.png', 'wb') as fw:
            await fw.write(dat)
    except Exception as e:
        print(e)


async def process_requests(urls: list[str], headers: dict):
    async with aiohttp.ClientSession(headers=headers) as s:
        await asyncio.gather(*(download_image(u, s) for u in urls))


def main():
    set_logger('downloaded_images.log')
    urls = ['https://c8.alamy.com/comp/WWH9YM/siberia-husky-sled-dog-dogphoto-dog-photo-dog-photos-WWH9YM.jpg',
            'https://thumbs.dreamstime.com/b/french-bulldog-small-breed-domestic-dog-were-result-s-cross-ancestors-imported-england-local-136021670.jpg',
            'https://images.all-free-download.com/images/graphiclarge/cute_dog_photo_picture_7_168843.jpg']
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_requests(urls, get_headers('headers.txt')))


if __name__ == '__main__':
    main()
