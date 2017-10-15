import pandas as pd

title_excludes = [ 'Crunch Report \|' ]

def exclude_articles(df):

    df_tech_crunch_idx = df['title'].str.contains('|'.join(title_excludes))
    df = df[~df_tech_crunch_idx]
    return df



