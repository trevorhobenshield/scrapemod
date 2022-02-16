import logging
from pathlib import Path

import httpx
import joblib
from bs4 import BeautifulSoup

from utils.utils import set_logger, get_headers, save_html


def get(url: str, headers: dict, client: httpx.Client) -> any:
    logging.debug(f"Downloading: {url}")
    try:
        data = client.get(url=url, headers=headers).text
        soup = BeautifulSoup(data, 'html.parser')
        print(soup)
        return soup
    except Exception as e:
        print(e)


def main():
    set_logger('mylog.log')
    urls = Path('urls.txt').read_text().splitlines()
    headers = get_headers('headers.txt')
    client = httpx.Client()
    res = joblib.Parallel(n_jobs=-1, prefer='threads')(joblib.delayed(get)(url, headers, client) for url in urls)
    save_html(res)


if __name__ == '__main__':
    main()
