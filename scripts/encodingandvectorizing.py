import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix

from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline, FeatureUnion

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.metrics import roc_curve

train = pd.read_csv('../assets/train.csv', index_col=0)
test = pd.read_csv('../assets/test.csv', index_col=0)

X_train = train[['artist', 'album', 'text', 'name']]
y_train = train['written_precoup']

X_test = test[['artist', 'album', 'text', 'name']]
y_test = test['written_precoup']


train_ind = X_train.index
test_ind = X_test.index

X_total = pd.concat([X_train, X_test], axis = 0, sort = True)
X_total = pd.get_dummies(X_total, columns=['artist', 'album'])
X_train = X_total.loc[train_ind, :]
X_test = X_total.loc[test_ind, :]

cvec = CountVectorizer()
cvec.fit(X_train['text'])

transformed_train = pd.DataFrame(cvec.transform(X_train['text']).todense(), columns=cvec.get_feature_names())
transformed_test = pd.DataFrame(cvec.transform(X_test['text']).todense(), columns=cvec.get_feature_names())

# X_train = pd.concat([transformed_train, X_train], axis = 1)
X_test = pd.concat([transformed_test, X_test], axis = 1)
# X_train.to_csv('X_train.csv')
X_test.to_csv('X_test.csv')
