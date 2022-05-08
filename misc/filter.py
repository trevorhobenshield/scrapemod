import time

import pandas as pd
from bs4 import BeautifulSoup
from joblib import Parallel, delayed


def fn(r):
    try:
        return pd.DataFrame({
            'col1': [r.select('.some_class')[0].text.strip()],
            'col2': [r.select('#some_id')[0].text.strip()],
            'url': [r.select('#scrape_url')[0].text.strip()]
        })
    except:
        ...


res: list[BeautifulSoup]

dfs = Parallel(n_jobs=-1, prefer='threads')(delayed(fn)(r) for r in res)
df = pd.concat(dfs)
# df.to_parquet(f'{time.time_ns()}.parquet')
df
