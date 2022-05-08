import re
from pathlib import Path
import pandas as pd

DATA_PATH = Path()

df = pd.concat([pd.read_parquet(d)for d in[f for f in DATA_PATH.iterdir()if'.parquet'in f.suffix]])

flags = re.I
term = 'regex expr'
res = (df
       .query('col1.str.contains(@term,regex=True,flags=@flags)', engine='python')
       .query('col2.str.contains("another expression",regex=True,flags=@flags)', engine='python')
       .sort_values('col3', ascending=False)
       .drop_duplicates('col4')
       .reset_index(drop=True)
       )
res