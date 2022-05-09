import logging
from pathlib import Path
import requests
from joblib import Parallel, delayed
from bs4 import BeautifulSoup
from utils import set_logger, save_soup, get_headers, tag_soup


def get(url: str, headers: dict, session: requests.Session) -> any:
    try:
        dat = session.get(url=url, headers=headers).content
        soup = tag_soup(BeautifulSoup(dat), url)
        save_soup(soup)
        return soup
    except Exception as e:
        logging.debug(f'Exception: {e} {url}')


def main():
    set_logger('downloaded_html.log')

    urls = Path('urls.txt').read_text().splitlines()
    session = requests.Session()
    headers = get_headers('headers.txt')
    res = Parallel(n_jobs=-1, prefer='threads')(delayed(get)(url, headers, session) for url in urls)


if __name__ == '__main__':
    main()
