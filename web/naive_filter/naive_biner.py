from bs4 import BeautifulSoup as sp
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
import json
from datetime import datetime
import os
import math
import pandas as pd
print("Program start at = ", datetime.now().time())



def preprocessing(berita):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    subs2 = '\s *\w\. |\(|\)|:|, |\.\n|”|“|…|\.  |&|\*|\?|"|- | -'
    subs3 = '\. |, |\/\n'
    substwith = '\n+|\s +'
    cleaning_words = re.sub(subs2, " ", berita)
    cleaning_words = re.sub(subs3, " ", cleaning_words)
    cleaning_words = re.sub(substwith, " ", cleaning_words)
    clean = cleaning_words.lower()
    tokenize = clean.split()
    token = " ".join(tokenize)
    return stemmer.stem(token)

def berita_terkategori():
    with open('../static/data_latih.json') as f:
        data = json.load(f)
    conter = 1
    berita = {}
    berita_hoax=[]
    berita_valid=[]
    doc_hoax ={}
    doc_valid ={}
    for item in data:
        if item['cat']=='hoax':
            news = preprocessing(item['berita'])
            news = news.split(' ')
            doc_hoax['doc'+str(conter)] = news
            conter+=1
        if item['cat']=='valid':
            news = preprocessing(item['berita'])
            news = news.split(' ')
            doc_valid['doc' + str(conter)] = news
            conter+=1
    berita['hoax']=doc_hoax
    berita['valid']=doc_valid

    if os.path.exists('../static/berita_cat_biner_tokenize.json'):
        os.remove('../static/berita_cat_biner_tokenize.json')
    with open('../static/berita_cat_biner_tokenize.json', 'w') as file:
        json.dump(berita, file)

def term_TerkategoriBiner():
    with open('../static/berita_cat_biner_tokenize.json') as files:
        data_tokenize = json.load(files)

    with open('../static/term_unik.json') as filess:
        term_unik = json.load(filess)

    all_term_cat = {}
    for label in data_tokenize:
        # print(label)
        all_kata = []
        beban_doc = {}
        for doc in data_tokenize[label]:
            # print(doc)
            for kata in data_tokenize[label][doc]:
                all_kata.append(kata)
        all_term_cat[label] = all_kata
    if os.path.exists('../static/kata_terkategori_biner.json'):
        os.remove('../static/kata_terkategori_biner.json')
    with open('../static/kata_terkategori_biner.json', 'w') as file:
        json.dump(all_term_cat, file)

berita_terkategori()
term_TerkategoriBiner()

# def conProbabilityBiner():
with open('../static/berita_cat_biner_tokenize.json') as files:
    data_tokenize = json.load(files)

with open('../static/term_unik.json') as filess:
    term_unik = json.load(filess)

with open('../static/kata_terkategori_biner.json') as filess:
    cat_biner = json.load(filess)

cons ={}
for label in data_tokenize:
    print(label)
    con = 0
    kata = {}
    for kata_unik in term_unik:
        Bt = 0
        NcW = 0
        if kata_unik in cat_biner[label]:
            Bt = 1
        for doc in data_tokenize[label]:
            kata_inDoc = data_tokenize[label][doc]
            if kata_unik in kata_inDoc:
                NcW+=1
        Nc = len(data_tokenize[label])
        # print(kata_unik)
        # print(Bt)
        # print(NcW)
        # print(Nc)
        # print('\n')
        consProbability = Bt*(NcW+1)/(Nc+2)+(1-Bt)*(1-(NcW+1)/(Nc+2))
        kata[kata_unik]=consProbability
    cons[label]=kata

if os.path.exists('../static/conproba_biner.json'):
    os.remove('../static/conproba_biner.json')
with open('../static/conproba_biner.json', 'w') as file:
    json.dump(cons, file)

print(pd.DataFrame(cons))

print("Program start at = ", datetime.now().time())
