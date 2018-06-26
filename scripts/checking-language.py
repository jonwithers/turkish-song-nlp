from common_words import get_list_of_tr_words_1, check_proportions
from lyrics_scraper import get_artists_list, master_scraper
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

import matplotlib.pyplot as plt
import seaborn as sns


# def check_if_turkish(text, dictionary):

def look_for_turkish_infixes(text):
    count = 0
    for word in text:
        word = word.lower()
        a_temp = word.find('iyor') != -1
        b_temp = word.find('ıyor') != -1
        c_temp = word.find('uyor') != -1
        d_temp = word.find('üyor') != -1
        if a_temp or b_temp or c_temp or d_temp:
            count +=1
    return count

def look_for_english(text):
    count = 0
    for word in text:
        if word.lower() == 'the' or word.lower() == 'for':
            count +=1
    return count

def look_for_french(text):
    count = 0
    for word in text:
        if word.lower() == "c'est" or word.lower() == 'un':
            count +=1
    return count


list_of_artists = ['candan-ercetin']#,'mogollar', 'ibrahim-tatlises', 'candan-ercetin']
df = master_scraper(list_of_artists)
list_of_lyrics = df['text']
df.to_csv('temp.csv')
dic = get_list_of_tr_words_1()

scores = []
for lyric in df['text']:
    if look_for_french(lyric.split(" ")) > 1:
        print('------------')
        print(lyric)
        print('------------')
        scores.append(0)
    else:
        scores.append(1)

sns.distplot(scores, kde = False)

plt.show()
