import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import pickle

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.metrics import roc_curve

from post_scraping_text_processing import *

df = pd.read_csv("../assets/lyrics/master_data_20180626.csv", index_col = 0)
df = clean_bad_langauge(df)

corpus = df['text'].copy()

years = pd.to_datetime(df['release']).dt.year
y = years.map(lambda x: 1 if x <2002 else 0)
cvec = CountVectorizer()
cvec.fit(corpus)
matrix = cvec.transform(corpus)
X = matrix.toarray()
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify = y)
try:
    with open('model.pkl', 'rb') as f:
        gnb = pickle.load(f)
except:
    gnb = GaussianNB()
    gnb.fit(X_train, y_train)
    with open('model.pkl', 'wb') as f:
        pickle.dump(gnb, f, pickle.HIGHEST_PROTOCOL)

sns.heatmap(confusion_matrix(y_test, gnb.predict(X_test)), fmt = 'g', annot = True)
plt.show()
tn, fp, fn, tp = confusion_matrix(y_test, gnb.predict(X_test)).ravel()

sens = tp/(tp + fn)
spec = tn/(tn + fp)
print('Sensitivity:',sens)
print('Specificity:',spec)
