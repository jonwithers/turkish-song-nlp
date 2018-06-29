import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from TurkishStemmer import TurkishStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import re
import time

from post_scraping_text_processing import remove_and_reg, split_into_words, remove_parens


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
corpus = corpus.map(remove_parens)
corpus = corpus.map(lambda x: x.lower().split())

def suffix_matchers(line, suffix_list):
    """Takes a line from the corpus and checks to see how many of the words have a certain ending (passes as a list to account for different morphological possibilities). This assumes that the lines are already lists. Could be fixed if more Turkish texts are going to be made."""
    suffix_count = 0
    suffix_length = len(suffix_list[0])
    for word in line:
        for suffix_possibility in suffix_list:
            suffix_count += word[-suffix_length:] == suffix_possibility
    return suffix_count

i = np.random.randint(0, len(corpus), 1)
print(corpus.iloc[i])

print(f"{suffix_matchers(corpus.iloc[i], ['ler', 'lar'])} words end in ler or lar")

print("{} words end in e or a".format(suffix_matchers(corpus.iloc[i], ['e', 'a'])))

print(f"{suffix_matchers(corpus.iloc[i], ['tur', 'dur', 'tür', 'dür', 'tir', 'dir', 'tır' 'dır'])} words end in DIr")

ts = TurkishStemmer()
corpus_stemmed = [ts.stem(j) for j in corpus.iloc[i]]
print(corpus_stemmed[0])

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
