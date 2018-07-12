import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from post_scraping_text_processing import clean_bad_language

def assemble(df):
    """takes a dataframe and creates training and testing sets"""
    df = clean_bad_language(df)
    df['year'] = pd.to_datetime(df['release']).dt.year
    df['written_before_2002'] = df['year'].map(lambda x: 1 if x <2002 else 0)
    df['written_before_2004'] = df['year'].map(lambda x: 1 if x <2002 else 0)
    df['written_before_2006'] = df['year'].map(lambda x: 1 if x <2002 else 0)
    df['written_before_2008'] = df['year'].map(lambda x: 1 if x <2002 else 0)
    df.to_csv('../assets/data/assembled_20180711.csv', index = True)

if __name__ == "__main__":
    df = pd.read_csv("../assets/lyrics/master_data_20180626.csv", index_col = 0)
    assemble(df)
