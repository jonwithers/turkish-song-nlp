#####
# Import the usual suspects for NLP plus many functions defined in
# post_scraping_text_processing (which itself imports from turkish_spacy_lemmatizer)
#####

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from TurkishStemmer import TurkishStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re
import time

from sklearn.feature_extraction.text import CountVectorizer

from post_scraping_text_processing import remove_and_reg, split_into_words, remove_punctuation, lemmatize

#####
# Read in data
# - transform data by removing unecessary columns
#####

df = pd.read_csv('../assets/lyrics/master_data_20180626.csv', index_col=0)
df.drop(['real_name', 'title', 'english_score'], axis = 1, inplace=True)

#####
# Set up the corpus
# - transform the corpus only by removing ads, getting rid of whitespace,
# - lowercasing, and splitting each line into a list of words.
#####

corpus = df['text'].copy()
corpus = corpus.map(remove_and_reg)
corpus = corpus.map(remove_punctuation)
corpus = corpus.map(lambda x: x.lower().split())

#####
# Bigram finder: there are several options here. The first uses the corpus as it is above.
# The second uses the spacy lemmatizer. The third uses the corpus with stopwords removed.
# All sets of bigrams are put into a pandas Series for counting and sorting.
#####

def get_bigrams(corp):
    """Assumes that the input is a list of lists, creates list of bigrams"""
    corp_sentences = list(corp.map(lambda x: " ".join(x)).values)
    return  pd.Series([b for l in corp_sentences for b in zip(l.split(" ")[:-1], l.split(" ")[1:])])

# Basic bigrams
basic_bigrams = get_bigrams(corpus)

# Lemmatized bigrams
lemmatized_corpus = corpus.map(lemmatize)
lemma_bigrams = get_bigrams(lemmatized_corpus)

# text = list(corpus.map(lambda x: " ".join(x)).values)

bigrams = [b for l in text for b in zip(l.split(" ")[:-1], l.split(" ")[1:])]
print(pd.Series(bigrams).value_counts(ascending=False)[:20])

# i_s = np.random.randint(0, len(corpus), 100)
#
# for i in i_s:
#     print(corpus.iloc[i])
#
#     print(f"{suffix_matchers(corpus.iloc[i], ['ler', 'lar'])} words end in ler or lar")
#
#     print("{} words end in e or a".format(suffix_matchers(corpus.iloc[i], ['e', 'a'])))
#
#     print(f"{suffix_matchers(corpus.iloc[i], ['tur', 'dur', 'tür', 'dür', 'tir', 'dir', 'tır' 'dır'])} words end in DIr")
#
#     time.sleep(4)
