import discogs_client
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import numpy as np

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
def check_for_english(text):
    text_words = text.split(" ")
    english_words = set(['I', "we're", "the", "an", "one", "to", "give", "love"])
    counter = 0
    for word in text_words:
        if word in english_words:
            counter += 1
    return counter

lyrics_df = pd.read_csv('../assets/lyrics/all_lyrics_scraped_20180625-155423.csv', index_col = 0)

lyrics_df['text'] = lyrics_df['text'].map(remove_and_reg)
lyrics_df['english_score'] = lyrics_df['text'].map(check_for_english)
tr_lyrics_df = lyrics_df[lyrics_df['english_score'] == 0]

release_discogs = []

songs = tr_lyrics_df['title']

total_songs = len(songs)
i = 1

d = discogs_client.Client('TurkishSongNLP/0.1')
d.set_consumer_key('DtigwAKfRYZIbHOXXqHd', 'zssaHwVHWvlzOAmayWHJzWhuTaUYchpE')

print(f"Get code from {d.get_authorize_url()[2]}")
d.get_access_token(input('Enter the authorization code: '))


for song in songs:
    try:
        release_discogs.append(d.release(d.search(song, type='release')[0].id).year)
        print(song, d.release(d.search(song, type='release')[0].id).year, f"{i} of {total_songs} scraped.")
    except:
        release_discogs.append(np.nan)
        print(f"Nothing to scrape. {i} of {total_songs} scraped.")
    time.sleep(1.2)
    i+=1

d = pd.DataFrame({
    'discog_year': release_discogs
})

d.to_csv('../assets/discog_year.csv')
