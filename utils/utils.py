import logging
import os
import time
from enum import Enum
from pathlib import Path
from typing import Optional,Callable
import functools
import pandas as pd


class LogConstants(Enum):
    FMT = '%(asctime)s.%(msecs)03d %(levelname)s:\t%(message)s'
    DT_FMT = '%Y-%m-%d %H:%M:%S'
    DT_FMT_ALT = '%Y.%m.%dD%H:%M:%S'


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
        df[new_col] = functools.reduce(lambda x,f:f(x), funcs, df[col])
    return df
