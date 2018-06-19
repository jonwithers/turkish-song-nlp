from common_words import get_list_of_tr_words_1, check_proportions
from lyrics_scraper import scrape_first_song_lyrics
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

lyrics_df = scrape_first_song_lyrics()
lyrics = lyrics_df['text'][0].split(" ")

lyrics_df2 = scrape_first_song_lyrics(url = 'http://sarki.alternatifim.com/sarkici/miley-cyrus/4x4-ftnelly')
lyrics2 = lyrics_df2['text'][0].split(" ")

dic = get_list_of_tr_words_1()

print(lyrics)
print(lyrics2)

print(check_proportions(lyrics, dic))
print(check_proportions(lyrics2, dic))
