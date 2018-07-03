import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

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

def remove_arabic(corpus):
    """Takes in corpus and returns corpus with arabic character lines removed"""
    return corpus[~corpus.str.contains('ض')]

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

#####

def grooming_language(df):
    """Takes a dataframe and performs 6 steps:
        - gets rid of unnecessary columns
        - gets rid of instrumental songs
        - replaces some dumb characters
        - gets rid on non-latin character songs
        - gets rid of Turkish non-latin character songs"""
    # Step 1: get rid of unnecessary columns, do initial corpus preparation
    df.drop(['real_name', 'title', 'english_score'], axis = 1, inplace=True)
    df.drop(28398, inplace = True)
    df['text'] = df['text'].map(remove_and_reg)
    df['text'] = df['text'].map(remove_punctuation)

    # Step 2: get rid of instrumental songs
    df = df[~(df['text'].str.contains('Şarkı enstrümantal olduğu için şarkı sözü bulunmamaktadır.'))]

    # Step 3: replace the weird x with regular x
    df['text'] = df['text'].str.replace('×', 'x')

    # Step 4: get rid of non-Latin songs
    non_latin_chars = '[ΌΓΜΝΤΧάέήίαγδεζηθικλμνοπρςτυφχψωόБГДЗКМНОПСТЧЩабвгдежзийклмнопрстуфхцчшщъюяѕابتجحخدذرزسشصضطعفقكلمنهوي]'
    df = df[~(df['text'].str.contains(non_latin_chars))]

    # Step 5: Replace some obvious non-issues
    df['text'] = df['text'].map(lambda x: x.replace('�', ''))
    df['text'] = df['text'].map(lambda x: x.replace('😂', ''))
    df['text'] = df['text'].map(lambda x: x.replace('²', ''))

    # Step 6: Take out the non-Turkish Latin-character songs
    latin_bad_chars_regex = '[åïß£ðÉ¡äžÓ¢ÁčÑéñ¿ëúìàËÈ®òÃ¶šőãýþèóæáÚœÛíùøª]'
    tr_bad_chars = [53589, 53602, 7199, 10877, 14731, 51120, 53602, 54753, 19378, 20366, 21101, 22154, 22157, 27489, 38708, 49124]
    non_turkish_index = df[df['text'].str.contains(latin_bad_chars_regex)].index
    non_turkish_index = df['text'][non_turkish_index].drop(tr_bad_chars).index
    df = df.drop(non_turkish_index)
    return df

def replace_weird_chars(text_col):
    text_col = text_col.str.replace('ä', 'a')
    text_col = text_col.str.replace('á', 'a')
    text_col = text_col.str.replace('ß', 'b')
    text_col = text_col.str.replace('Ã¢', 'a')
    text_col = text_col.str.replace('É', 'E')
    text_col = text_col.str.replace('Ã‚', 'A')
    text_col = text_col.str.replace('é', 'e')
    text_col = text_col.str.replace('ð', 'ğ')
    text_col = text_col.str.replace('w', 'v')
    text_col = text_col.str.replace('göanül', 'gönül')
    text_col = text_col.str.replace('ú', 'u')
    text_col = text_col.str.replace('ý', 'ı')
    text_col = text_col.str.replace('í', 'i')
    text_col = text_col.str.replace('Söz  Fikret Şeneş & Müzik  Diques Fleche', '')
    text_col = text_col.str.replace('Icqum 150' , '')
    text_col = text_col.str.replace('Montesquieuyu' , '')
    return text_col

def drop_more_wrong_language(df):
    df.drop(df[df['text'].str.contains('qu')].index, inplace = True)
    df.drop(df[(df['text'].str.contains('of') & df['text'].str.contains('my')) | (df['text'].str.contains('the') & df['text'].str.contains('you'))].index, inplace = True)
    df.drop(df[(df['text'].str.contains('your'))].index, inplace = True)
    df.drop(df[(df['text'].str.contains(' for '))].index, inplace = True)
    df.drop(df[(df['text'].str.contains(' For '))].index, inplace = True)
    df.drop(df[(df['text'].str.contains(' With '))].index, inplace = True)
    df.drop(df[(df['text'].str.contains(' love '))].index, inplace = True)
    df.drop(df[(df['text'].str.contains('Love'))].index, inplace = True)
    df.drop(df[(df['text'].str.contains(' çi '))].index, inplace = True)
    df = df[df['artist'] != 'Agire Jiyan']
    df = df[df['artist'] != 'Abidin Biter']
    return df

def clean_bad_langauge(df):
    """Wrapper for grooming_langauge, replace_weird_chars, and drop_more_wrong_language"""
    df = grooming_language(df)
    df['text'] = replace_weird_chars(df['text'])
    df = drop_more_wrong_language(df)
    return df

if __name__ == '__main__':
    if sys.argv[1] == 'functions':
        print('functions loaded')
    else:
        df = pd.read_csv("../assets/lyrics/master_data_20180626.csv", index_col = 0)
        df = clean_bad_langauge(df)
        print('df loaded.')
        print(f'{df.shape[0]} rows x {df.shape[1]} columns')
