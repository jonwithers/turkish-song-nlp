import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
from post_scraping_text_processing import remove_and_reg
import numpy as np

client_credentials_manager = SpotifyClientCredentials(client_id = '82b857bc19b8402dbf050cc433158f42', client_secret = '799bcde8e32b40ceaa19793845087b5f')
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

lyrics_df = pd.read_csv('../assets/lyrics/all_lyrics_scraped_20180625-155423.csv', index_col = 0)

lyrics_df['text'] = lyrics_df['text'].map(remove_and_reg)
lyrics_df['english_score'] = lyrics_df['text'].map(check_for_english)
tr_lyrics_df = lyrics_df[lyrics_df['english_score'] == 0]

release_spotify = []
name_spotify = []
songs = tr_lyrics_df['title']
artists = tr_lyrics_df['artist']
total_songs = len(songs)
i = 1
for song, artist in zip(songs, artists):
    r = sp.search(q = song+" "+artist, limit = 1)
    if len(r['tracks']['items']) == 0:
        release_spotify.append(np.nan)
        name_spotify.append(np.nan)
        print('Nothing to scrape', f"{i} / {total_songs} scraped")
    else:
        release_spotify.append(r['tracks']['items'][0]['album']['release_date'])
        name_spotify.append(r['tracks']['items'][0]['name'])
        print('Scraped', r['tracks']['items'][0]['name'], f"{i} / {total_songs} scraped")
    i+=1
    time.sleep(0.5)

output_df = pd.DataFrame({
    'release':release_spotify,
    'name': name_spotify,
    'real_name': songs
})

output_df.to_csv('../assets/lyrics_with_spotify.csv')
