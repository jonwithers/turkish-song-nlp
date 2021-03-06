from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import csv
import time

def scrape_first_song_lyrics(url = 'http://sarki.alternatifim.com/sarkici/sezen-aksu/1980'):
    results = requests.get(url)
    if results.status_code != 200:
        print("error")


    soup = BeautifulSoup(results.content, 'lxml')

    artist_and_song_title = soup.find('h3', {'class':'baslik'}).text

    artist = artist_and_song_title.split('-')[0].strip()
    song_title = artist_and_song_title.split('-')[1].strip()

    album_title = soup.find('tr').find('td', {'style':None}).text

    song_text = soup.find('div', {"class":'sarkisozu'}).text

    song_text = song_text[:song_text.find('*')].replace('\r', '').replace('\n', ' ').replace('/','')

    print("Artist: ", artist)
    print("Song Title: ", song_title)
    print("Album: ", album_title)

    artist_col = []
    title_col = []
    album_col = []
    text_col = []

    artist_col.append(artist)
    title_col.append(song_title)
    album_col.append(album_title)
    text_col.append(song_text)

    return pd.DataFrame({'artist': artist_col,
        'title': title_col,
        'album': album_col,
        'text': text_col
    })

def get_artists_list(artist_name='sezen-aksu'):
    songlist = []
    for i in range(1,100):
        url = 'http://sarki.alternatifim.com/sarkici/' + artist_name + '/sayfa-' + str(i)
        results = requests.get(url)
        if results.status_code !='200':
            pass
        print("Scraping", url)
        soup = BeautifulSoup(results.content, 'lxml')
        try:
            list_items = soup.find('ul').find_all('li')
            this_list = [i.find('a').attrs['href'] for i in list_items]
            songlist+=this_list
        except:
            return songlist
    return songlist

def master_scraper(list_of_artists=[]):
    artist_col = []
    title_col = []
    album_col = []
    text_col = []
    timestr = time.strftime("%Y%m%d-%H%M%S")
    # master_list = []
    # for artist in list_of_artists:
    #     master_list += get_artists_list(artist)
    # pd.DataFrame({'master_list':master_list}).to_csv('assets/master_list.csv', index = False)
    master_list = pd.read_csv('assets/master_list.csv', header = None, names = ['master_list'], skiprows = 46065)['master_list']
    for item in master_list:
        url = 'http://sarki.alternatifim.com' + item
        results = requests.get(url)
        if results.status_code != 200:
            print('Scrape failed')
            pass
        print("Scraping", url)
        soup = BeautifulSoup(results.content, 'lxml')
        try:
            important_content = soup.find('div', {'class': 'ten columns cleft yazim'})
            title_info = important_content.find('div', {'class':'cbottom'})
            artist_and_song_title = title_info.find('h3').text
            artist = artist_and_song_title.split('-')[0].strip()
            song_title = artist_and_song_title.split('-')[1].strip()
            try:
                album_title = title_info.find('table').find('tbody').find('tr').find_all('td')[2].text
            except:
                album_title = np.nan

            song_text = important_content.find('div', {"class":'sarkisozu'}).text.strip()
            if song_text.find("<!--") != -1:
                song_text = song_text[:song_text.find("<!--")]
            song_text = song_text[:song_text.find('/*')].replace('\r', ' ').replace('\n', '  ').replace('/',' ')
        except:
            pass
        artist_col.append(artist)
        title_col.append(song_title)
        album_col.append(album_title)
        text_col.append(song_text)

        this_row = [artist, song_title, album_title, song_text]
        with open('assets/' + timestr + '_test.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(this_row)
    return pd.DataFrame({
        'artist':artist_col,
        'title':title_col,
        'album':album_col,
        'text':text_col
    })

# list_of_artists = ['sezen-aksu','mogollar', 'ibrahim-tatlises', 'candan-ercetin', 'mor-ve-otesi', 'tarkan', 'orhan-gencebay', 'bulent-ersoy', 'zeki-muren', 'ahmet-kaya', 'kazim-koyuncu', 'baris-manco', 'sibel-can', 'murat-boz', 'sertab-erener', 'metin-ersoy', 'sebnem-ferah', 'muslum-gurses']

if __name__ == '__main__':
        # list_of_artists = pd.read_csv('assets/list_of_artists.csv')['artist']
        df = master_scraper()
        print('scraped {} songs'.format(df.shape[0]))

        timestr = time.strftime("%Y%m%d-%H%M%S")
        df.to_csv("assets/lyrics/all_lyrics_scraped_"+timestr+".csv")
