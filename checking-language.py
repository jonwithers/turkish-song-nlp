from common_words import get_list_of_tr_words_1, check_proportions
from lyrics_scraper import get_artists_list, master_scraper
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

list_of_artists = ['sezen-aksu']#,'mogollar', 'ibrahim-tatlises', 'candan-ercetin']
df = master_scraper(list_of_artists)
list_of_lyrics = df['text']

dic = get_list_of_tr_words_1()

scores = []
for lyric in list_of_lyrics:
    scores.append(check_proportions(lyric.split(" "), dic))

import matplotlib.pyplot as plt
import seaborn as sns

sns.distplot(scores)

plt.show()
