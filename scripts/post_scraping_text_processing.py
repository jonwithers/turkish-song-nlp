import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from TurkishStemmer import TurkishStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import re
from turkish_spacy_lemmatizer import LOOKUP
from spacy_stop_words import STOP_WORDS

def remove_ads(text):
    """Removes the ads that somehoe got scraped from alternatifim"""
    pattern = r'(eval.*])'
    return re.sub(pattern, "", text)

def regularize_whitespace(text):
    """Perhaps unnecessary, but removes whitespace"""
    whitepattern = r'\s+'
    return re.sub(whitepattern, " ", text).strip()

def remove_and_reg(text):
    """Removes ads, regularizes whitespace"""
    text = remove_ads(text)
    text = regularize_whitespace(text)
    return text

def split_into_words(text):
    """splits into words using basic string method"""
    text.split(" ")

def join_into_sentence(text):
    """joins a list of words into a single sentence string"""
    " ".join(text)

def remove_chars(text, char_list):
    """takes a text and a string of characters to remove and removes them"""
    for char in char_list:
        text = text.replace(char, "")
    return text

def remove_punctuation(text):
    """uses remove_chars to remove basic punctuation."""
    return remove_chars(text, '()",.;:!?\'\\/')

def suffix_matchers(line, suffix_list):
    """Takes a line from the corpus and checks to see how many of the words have a certain ending (passes as a list to account for different morphological possibilities). This assumes that the lines are already lists. Could be fixed if more Turkish texts are going to be made."""
    suffix_count = 0
    suffix_length = len(suffix_list[0])
    for word in line:
        for suffix_possibility in suffix_list:
            suffix_count += word[-suffix_length:] == suffix_possibility
    return suffix_count

def lemmatize(line):
    """Uses the spacy Turkish lemmatizer to lemmatize words in a list"""
    return_list = []
    for word in line:
        try:
            return_list.append(LOOKUP[word])
        except:
            return_list.append(word)
    return return_list

def remove_turkish_stopwords(text):
    """removes stopwords using the set from spacy. input text is a list of words."""
    return [word for word in text if word not in STOP_WORDS]
    
if __name__ == '__main__':
    print("Working")
