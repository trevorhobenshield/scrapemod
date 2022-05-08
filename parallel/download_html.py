import logging
from pathlib import Path
import requests
import joblib
from bs4 import BeautifulSoup

from utils import set_logger, save_html, get_headers


def get(url: str, headers: dict, session: requests.Session) -> any:
    try:
        dat = session.get(url=url, headers=headers).content
        soup = BeautifulSoup(dat)
        p = soup.new_tag('p', id='scrape_url')
        p.string = url
        soup.html.body.insert(0, p)
        save_html(soup)
        return soup
    except Exception as e:
        logging.debug(f'Exception: {e} {url}')


def main():
    set_logger('downloaded_webpages.log')
    urls = Path('urls.txt').read_text().splitlines()
    session = requests.Session()
    res = joblib.Parallel(n_jobs=-1, prefer='threads')(joblib.delayed(get)(url, get_headers('headers.txt'), session) for url in urls)
    [save_html(r) for r in res]


if __name__ == '__main__':
    main()
