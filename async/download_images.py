from pathlib import Path
import hashlib
import logging
import aiofiles
import asyncio
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
    urls: list[str] = Path('urls.txt').read_text().splitlines()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_requests(urls, get_headers('headers.txt')))


if __name__ == '__main__':
    main()
