from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import time

def scrape_a_letter(letter):
    """Scrapes the artist slugs given a letter of the alphabet"""

    slugs = []

    for i in range(1,100):
        url = 'http://sarki.alternatifim.com/populer-sarkicilar/' + letter + "/sayfa-" + str(i)
        results = requests.get(url=url)
        if results.status_code != '200':
            pass
        print("Scraping", url)
        soup = BeautifulSoup(results.content, 'lxml')


        try:
            table_of_singers = soup.find("div", {"class":"sarkisozu"}).find_all("ul")
            for table in table_of_singers:
                rows = table.find_all("li")
                for item in rows:
                    if item.find("a")['href'].replace("/sarkici/", "") != '/sarkicilar/'+letter:
                        print(item.find("a")['href'].replace("/sarkici/", ""))
                        slugs.append(item.find("a")['href'].replace("/sarkici/", ""))
        except:
            return slugs


    return slugs

if __name__ == "__main__":
    list_of_letters = [i for i in "ABCÇDEFGHIİJKLMNOÖPRSŞTUÜVYZ"]
    list_of_artists = []
    for letter in list_of_letters:
        list_of_artists += scrape_a_letter(letter)
    pd.DataFrame({'artist':list_of_artists}).to_csv('assets/list_of_artists.csv', index = False)
