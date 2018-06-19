from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd

def get_list_of_tr_words_1():
    url = 'https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Turkish_wordlist'

    results = requests.get(url)
    # print(results.status_code)

    soup = BeautifulSoup(results.content, 'lxml')

    list = soup.find('div', {'class':'mw-parser-output'}).find_all('p')[1].text
    list = list.splitlines()
    list2 = []
    for item in list:
        item = item[:item.find(" ")]
        list2.append(item)
    # list_of_words = []
    # for row in tabl.find_all('li'):
    #     els = row.find('a')
    #     list_of_words.append(els.text)
    return list2

def check_proportions(text, dic):
    count = 0
    text_length = len(text)

    for word in text:
        count += word.lower() in dic

    print(count/text_length)
    return(count/text_length)

def get_list_of_tr_words():
    filename = 'tr.txt'
    dic_list = []
    with open(filename, 'r') as f:
        for line in f:
            dic_list.append(line[:line.find(" ")])
    return dic_list


if __name__ == "__main__":
    print(get_list_of_tr_words_1())
    # dic = get_list_of_tr_words()
    # te = ['bir','gün', 'I' 'was', 've', 'iki']
    # print(dic)
    # check_proportions(te, dic)
