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

from post_scraping_text_processing import remove_and_reg, split_into_words, remove_punctuation, lemmatize, remove_turkish_stopwords

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

def get_bigrams(corp, repeats = True):
    """Assumes that the input is a list of lists, creates pandas Series of bigrams"""
    corp_sentences = list(corp.map(lambda x: " ".join(x)).values)
    if repeats:
        return pd.Series([b for l in corp_sentences for b in zip(l.split(" ")[:-1], l.split(" ")[1:])])
    else:
        return pd.Series([b for l in corp_sentences for b in zip(l.split(" ")[:-1], l.split(" ")[1:]) if b[0] != b[1]])

#####
# Each of the following creates a list of the top 20 bigrams given conditions
#####


# Basic bigrams: No additional processing
basic_bigrams = get_bigrams(corpus)

# Lemmatized bigrams
lemmatized_corpus = corpus.map(lemmatize)
lemma_bigrams = get_bigrams(lemmatized_corpus)

destopped_corpus = corpus.map(remove_turkish_stopwords)
destopped_bigrams = get_bigrams(destopped_corpus)

print("Basic bigrams:\n----------")
print(basic_bigrams.value_counts()[:20])
print("Bigrams from lemmatized corpus:\n----------")
print(lemma_bigrams.value_counts()[:20])
print("Bigrams from corpus without stopwords:\n----------")
print(destopped_bigrams.value_counts()[:20])
print("")

basic_bigrams = get_bigrams(corpus, repeats = False)

# Lemmatized bigrams
lemmatized_corpus = corpus.map(lemmatize)
lemma_bigrams = get_bigrams(lemmatized_corpus, repeats = False)

destopped_corpus = corpus.map(remove_turkish_stopwords)
destopped_bigrams = get_bigrams(destopped_corpus, repeats = False)


print("Basic bigrams without repetition:\n----------")
print(basic_bigrams.value_counts()[:20])
print("Bigrams from lemmatized corpus without repetition:\n----------")
print(lemma_bigrams.value_counts()[:20])
print("Bigrams from corpus without stopwords or repetition:\n----------")
print(destopped_bigrams.value_counts()[:20])
print("")

really_stripped_corpus = corpus.map(remove_turkish_stopwords).map(lemmatize)
really_stripped_bigrams = get_bigrams(really_stripped_corpus, repeats = False)
print("Bigrams from corpus without stopwords, lemmatized, and no repetition")
print(really_stripped_bigrams.value_counts()[:20])

even_more_stripped_corpus = really_stripped_corpus.map(lambda x: [word for word in x if word != 'bir'])
even_more_stripped_bigrams = get_bigrams(even_more_stripped_corpus, repeats = False)
print("Bigrams from corpus without stopwords, lemmatized, no repetition, and no word bir")
print(even_more_stripped_bigrams.value_counts()[:20])
