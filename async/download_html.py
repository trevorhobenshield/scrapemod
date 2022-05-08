from pathlib import Path
import logging
import aiohttp
import asyncio
import uvloop
import nest_asyncio
from bs4 import BeautifulSoup

from utils import set_logger, get_headers, save_html

nest_asyncio.apply()  # needed if running in notebook
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())  # modified event loop


async def get(url: str, session: aiohttp.ClientSession) -> BeautifulSoup:
    try:
        logging.debug(f'Downloading: {url}')
        response = await session.request(method='GET', url=url)
        dat = await response.text()
        soup = BeautifulSoup(dat)
        p = soup.new_tag('p', id='scrape_url')
        p.string = url
        soup.html.body.insert(0, p)
        save_html(soup)  # save html to data/*.html
        return soup
    except Exception as e:
        print(e)


async def process_requests(urls: list, headers: dict) -> list:
    async with aiohttp.ClientSession(headers=headers) as s:
        return await asyncio.gather(*(get(u, s) for u in urls))


def main():
    set_logger('downloaded_webpages.log')
    urls: list[str] = Path('urls.txt').read_text().splitlines()
    loop = asyncio.get_event_loop()
    res: list[BeautifulSoup] = loop.run_until_complete(process_requests(urls, get_headers('headers.txt')))


if __name__ == '__main__':
    main()
