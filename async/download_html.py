from pathlib import Path
import logging
import aiohttp
import asyncio
import uvloop
import nest_asyncio
from bs4 import BeautifulSoup

from utils import set_logger, get_headers, save_soup, tag_soup

nest_asyncio.apply()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def get(url: str, session: aiohttp.ClientSession) -> BeautifulSoup:
    try:
        logging.debug(f'Downloading: {url}')
        response = await session.request(method='GET', url=url)
        dat = await response.text()
        soup = tag_soup(BeautifulSoup(dat), url)
        save_soup(soup)
        return soup
    except Exception as e:
        print(e)


async def process_requests(urls: list, headers: dict) -> list:
    async with aiohttp.ClientSession(headers=headers) as s:
        return await asyncio.gather(*(get(u, s) for u in urls))


def main():
    set_logger('downloaded_html.log')
    urls: list[str] = Path('urls.txt').read_text().splitlines()
    loop = asyncio.get_event_loop()
    res: list[BeautifulSoup] = loop.run_until_complete(process_requests(urls, get_headers('headers.txt')))


if __name__ == '__main__':
    main()
