import logging
import os
import time
from enum import Enum
from pathlib import Path
from typing import Optional, Callable
import functools
import pandas as pd
import exif
from bs4 import BeautifulSoup


class Dirs(Enum):
    DATA = Path('data')
    LOGS = Path('logs')


class LogConstants(Enum):
    FMT = '%(asctime)s.%(msecs)03d %(levelname)s:\t%(message)s'
    DT_FMT = '%Y-%m-%d %H:%M:%S'
    DT_FMT_ALT = '%Y.%m.%dD%H:%M:%S'


class ImageCustom(exif.Image):
    def __init__(self, img_file):
        super().__init__(img_file)

    def dirty_delete(self) -> None:
        for _ in range(2):
            for tag in self._segments["APP1"].get_tag_list():
                try:
                    self.__delattr__(tag)
                except Exception as e:
                    print(e)
            self._parse_segments(self.get_file())


def exif_strip(imgs_path: str):
    for file in Path(imgs_path).iterdir():
        try:
            img = ImageCustom(Path(file).read_bytes())
            img.dirty_delete()
            (file.parent / f'{file.stem}_MODIFIED{file.suffix}').write_bytes(img.get_file())
        except Exception as e:
            print(e)


def set_logger(filename: str) -> None:
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.basicConfig(
        filename=f'logs/{filename}',
        filemode='a',
        level=logging.DEBUG,
        format=LogConstants.FMT.value,
        datefmt=LogConstants.DT_FMT_ALT.value)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt=LogConstants.FMT.value,
                                  datefmt=LogConstants.DT_FMT_ALT.value)
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)


def save_soup(soup: BeautifulSoup, filename: Optional[str] = None) -> None:
    os.makedirs(Dirs.DATA.value) if not os.path.exists(Dirs.DATA.value) else ...
    name = f'{filename}-' if filename else ''
    with open(Dirs.DATA.value / f"{name}{time.time_ns()}.html", 'w', encoding='utf-8') as fw:
        fw.write(soup.prettify())


def tag_soup(soup:BeautifulSoup, url:str) -> BeautifulSoup:
    p = soup.new_tag('p', id='scrape_url')
    p.string = url
    soup.html.body.insert(0, p)
    return soup

def get_headers(fname: str) -> dict:
    """
    Parse headers directly copied from dev tools.
    """
    return {t[0].lower(): t[-1].strip()
            for t in (s.partition(':')
                      for s in Path(fname).read_text().split('\n') if s)}


def tfm(df: pd.DataFrame, transforms: list[list[str, str, Callable]]) -> pd.DataFrame:
    """
    Apply n transformations to k columns of a DataFrame

    -----------------------------------------------------------------
    Example:
    -----------------------------------------------------------------
    tfm(df, [
        ['price', 'price_T', [
            (lambda x: x.str.replace('[\$,]', '', regex=True)),
            (lambda x: x.astype('float'))
        ]],
        ['date', 'date_T', [
            (lambda x: pd.to_datetime(x))
        ]],
    ])
    """
    for col, new_col, funcs in transforms:
        df[new_col] = functools.reduce(lambda x, f: f(x), funcs, df[col])
    return df
