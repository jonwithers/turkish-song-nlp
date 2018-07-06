import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from post_scraping_text_processing import clean_bad_language

def make_train_and_test(df):
    """takes a dataframe and creates training and testing sets"""
    df = clean_bad_language(df)
    years = pd.to_datetime(df['release']).dt.year
    df['written_precoup'] = years.map(lambda x: 1 if x <2002 else 0)
    target = 'written_precoup'
    features = [i for i in df.columns if (i != target) and (i != 'release')]
    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify = y)
    train = pd.concat([X_train, y_train], axis=1)
    train.to_csv('../assets/train.csv', index=True)
    test = pd.concat([X_test, y_test], axis = 1)
    test.to_csv('../assets/test.csv', index = True)

if __name__ == "__main__":
    df = pd.read_csv("../assets/lyrics/master_data_20180626.csv", index_col = 0)
    make_train_and_test(df)
