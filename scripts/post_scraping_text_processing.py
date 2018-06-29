import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from TurkishStemmer import TurkishStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import re

def remove_ads(text):
    pattern = r'(eval.*])'
    return re.sub(pattern, "", text)

def regularize_whitespace(text):
    whitepattern = r'\s+'
    return re.sub(whitepattern, " ", text).strip()

def remove_and_reg(text):
    text = remove_ads(text)
    text = regularize_whitespace(text)
    return text

def split_into_words(text):
    text.split(" ")

def remove_parens(text):
    text = text.replace("(", "").replace(")", "")
    return text

def remove_periods(text):
    text = text.replace(".", "")
    return text
    
if __name__ == '__main__':
    print("Working")
