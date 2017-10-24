import pandas as pd

title_excludes = [ 'Crunch Report \|' ]

url_excludes = [ '\/video\/']
def exclude_articles(df):
    df_text_exclude_idx = df['text'].str.len() < 400
    df_title_exclude_idx = df['title'].str.contains('|'.join(title_excludes))
    df_url_exclude_idx = df['url'].str.contains('|'.join(url_excludes))
    df = df[~(df_title_exclude_idx | df_url_exclude_idx | df_text_exclude_idx )]
    return df



