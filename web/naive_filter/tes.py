from bs4 import BeautifulSoup as sp
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
import json
from datetime import datetime
import os
import math

print("Program start at = ", datetime.now().time())

factory = StemmerFactory()
stemmer = factory.create_stemmer()

subs2 = '\s *\w\. |\(|\)|:|, |\.\n|”|“|…|\.  |&|\*|\?|"|- | -'
subs3 ='\. |, |\/\n'
substwith= '\n+|\s +'

path_offData = '../offData/dataset.txt'

def preprocessing(berita):
    cleaning_words = re.sub(subs2, " ", berita)
    cleaning_words = re.sub(subs3, " ", cleaning_words)
    cleaning_words = re.sub(substwith, " ", cleaning_words)
    clean = cleaning_words.lower()
    tokenize = clean.split()
    token = " ".join(tokenize)
    return stemmer.stem(token)

all_data=[]
file = open(path_offData, encoding="utf8")
soup = sp(file,'html5lib')
doc_berita = soup.find_all("doc")
counter_duplicat = 0

list_judul = []
for item in doc_berita:
    data = {}
    juduls = item.find('judul').text
    cats = item.find('cat').text
    beritas = item.find('berita').text

    judul_filter = preprocessing(juduls)
    data['judul'] = juduls
    data['cat'] = cats
    data['berita'] = beritas

    if judul_filter not in list_judul:
        list_judul.append(preprocessing(juduls))
        all_data.append(data)
    else:counter_duplicat+=1

print(counter_duplicat)
print(len(all_data))

print("Program start at = ", datetime.now().time())
