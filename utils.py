import logging
import os
import time
from enum import Enum
from pathlib import Path
from typing import Optional, Callable
import functools
import pandas as pd
import exif
import random
from user_agents import USER_AGENTS

BASE_HEADERS = {
    'User-Agent': random.choice([
        *USER_AGENTS['Chrome'],
        *USER_AGENTS['Firefox'],
        *USER_AGENTS['Safari'],
        *USER_AGENTS['Edge'],
        *USER_AGENTS['Vivaldi'],
    ]),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
}


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


def save_html(data: list, filename: Optional[str] = None) -> None:
    out_path = Path('out')
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    name = f'{filename}-' if filename else ''
    for soup in data:
        with open(out_path / f"{name}{time.time_ns()}.html", 'w', encoding='utf-8') as fw:
            fw.write(soup.prettify())


def get_headers(fname: str) -> dict:
    return {t[0].lower(): t[-1].strip()
            for t in (s.partition(':')
                      for s in Path(fname).read_text().split('\n') if s)}


def tfm(df: pd.DataFrame, transforms: list[list[str, str, Callable]]) -> pd.DataFrame:
    """
    
    E.g.
    
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
