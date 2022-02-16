import pandas as pd


# https://tomaugspurger.github.io/archives.html

################################################################################################################
### Using functools ###
# df.columns = reduce(lambda r,f: f(r), [
#     lambda x: x.str.replace('[\W]','_'),
#     lambda x: x.str.replace('_{2,}','_'),
# ], df.columns)

### Using pandas pipe ###
# df.columns = (
#     pd.Series(df.columns)
#         .pipe(lambda x: x.str.replace('[\W]','_'))
#         .pipe(lambda x: x.str.replace('_{2,}','_'))
# )
# df.columns
################################################################################################################
# for c in col_list_types:
#     df[c] = (df[c]
#     .pipe(lambda x: x.explode(ignore_index=True))
#     .pipe(lambda x: x.astype('category'))
#     )
# df
################################################################################################################
# res = ...
# df = (pd.concat([pd.concat(_) for _ in res], axis=1)
#       .reset_index(drop=True)
#       .pipe(lambda _: _.replace(r'(\n)+', '', regex=True))
#       .assign(days_ago=lambda x: (x['date']
#                                   .pipe(lambda _: _.str.extract('(\d+)'))
#                                   .pipe(lambda _: pd.Series(_.to_numpy().ravel()).str.zfill(2))))
#       )
# df_final = df.loc[:, ~df.columns.duplicated()]
################################################################################################################
# df = pd.read_csv('../data/mathGrade.csv')
# cols_before = df.columns
#
#
# df.columns = (df.columns.to_series()
#     .pipe(lambda _:_.str.replace('[%]+',' Pct ',regex=True))
#     .pipe(lambda _:_.str.replace('[\W_]+',' ',regex=True))
#     .pipe(lambda _:_.str.title())
#     .pipe(lambda _:_.str.replace(' ',''))
# )
#
# pd.DataFrame({'before':cols_before,'after':df.columns})
################################################################################################################
# df = df.assign(new_col=df['coolness']
#                .str.replace(r'[!\.]+', '')
#                .map({'satisfactory': 'ST', 'cool': 'CL'})
#                # another chained operation
#                # ...
#                # another chained operation
#                .dropna()
#                .astype('category'))
# df
################################################################################################################
# df = df.assign(
#     new_col_2=df.apply(
#         lambda x: 'lame' if pd.notnull(x['coolness']) and x['coolness'].lower() == 'uncool' else 'cool enough', axis=1
#     )
# )
################################################################################################################
# def foo(x):
#     return x.height * 100
#
# bar = lambda x: x.name.str.upper()
#
#
# df = df.assign(
#     height_cm=foo,
#     height_inches=lambda x: x.height_cm / 2.54, # ok
#     big_name=bar
# )
#
# view(df)
################################################################################################################
# df = pd.read_csv('people.csv')
#
# def height_conversion(df):
#     temp = df.copy()
#     temp = temp.assign(
#         height_cm=lambda x: x['height'] * 100,
#         height_inches=lambda x: x['height_cm'] / 2.54
#     )
#     return temp
#
# def title_name(df):
#     temp = df.copy()
#     return temp.assign(title_name=lambda x: x['name'].str.title())
#
# def some_func(df,p,q):
#     temp = df.copy()
#     return temp.assign(some_col=lambda x: x.name+f'{p}{q}')
#
# new_df = (
#     df.pipe(height_conversion)
#       .pipe(title_name)
#       .pipe(some_func, p=420,q=69)
# )
# new_df
################################################################################################################
