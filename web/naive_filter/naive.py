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

path_offData = '../offData/800.txt'

def preprocessing(berita):
    cleaning_words = re.sub(subs2, " ", berita)
    cleaning_words = re.sub(subs3, " ", cleaning_words)
    cleaning_words = re.sub(substwith, " ", cleaning_words)
    clean = cleaning_words.lower()
    tokenize = clean.split()
    token = " ".join(tokenize)
    return stemmer.stem(token)

def openFile(pathdata,ratio):
    all_data=[]
    file = open(pathdata, encoding="utf8")
    soup = sp(file,'html5lib')
    doc_berita = soup.find_all("doc")
    for item in doc_berita:
        data = {}
        juduls = item.find('judul').text
        cats = item.find('cat').text
        beritas = item.find('berita').text

        data['judul'] = juduls
        data['cat'] = preprocessing(cats)
        data['berita'] = beritas
        all_data.append(data)

    counter = 0
    counter_hoax = 0
    counter_valid = 0

    for item in all_data:
        if item['cat'] == 'valid':
            counter_valid += 1
        if item['cat'] == 'hoax':
            counter_hoax += 1

    if counter_valid < counter_hoax:
        counter = counter_valid
    else:
        counter = counter_hoax

    data_hoax = []
    data_valid = []

    for item in all_data:
        temp = {}
        if len(data_hoax) != counter and item['cat'] == 'hoax':
            temp['judul'] = item['judul']
            temp['cat'] = item['cat']
            temp['berita'] = item['berita']
            data_hoax.append(temp)
        if len(data_valid) != counter and item['cat'] == 'valid':
            temp['judul'] = item['judul']
            temp['cat'] = item['cat']
            temp['berita'] = item['berita']
            data_valid.append(temp)

    uji_hoax = []
    uji_valid = []

    data_balance = data_hoax+data_valid
    total_data = len(data_hoax + data_valid)
    ratio = (total_data / 2) * ratio / 2

    for i in range(int(ratio)):
        uji_hoax.append(data_hoax.pop())
    for i in range(int(ratio)):
        uji_valid.append(data_valid.pop())

    data_uji = uji_hoax + uji_valid
    data_latih = data_hoax + data_valid



    if os.path.exists('../static/data_uji.json'):
        os.remove('../static/data_uji.json')
    with open('../static/data_uji.json', 'w') as uji:
        json.dump(data_uji,uji)

    if os.path.exists('../static/data_latih.json'):
        os.remove('../static/data_latih.json')
    with open('../static/data_latih.json', 'w') as latih:
        json.dump(data_latih,latih)

    if os.path.exists('../static/data_balance.json'):
        os.remove('../static/data_balance.json')
    with open('../static/data_balance.json', 'w') as balance:
        json.dump(data_balance,balance)

def berita_terkategori(data):
    berita = {}
    berita_hoax=[]
    berita_valid=[]
    for item in data:
        if item['cat']=='hoax':
            berita_hoax.append(preprocessing(item['berita']))
        if item['cat']=='valid':
            berita_valid.append(preprocessing(item['berita']))
    berita['hoax']=berita_hoax
    berita['valid']=berita_valid

    if os.path.exists('../static/berita_cat.json'):
        os.remove('../static/berita_cat.json')
    with open('../static/berita_cat.json', 'w') as file:
        json.dump(berita, file)

def termUnik():
    with open("../offData/stopword2016.txt", "r") as stopword:
        stopword = stopword.read().splitlines()
    with open('../static/berita_cat.json') as files:
        data_berita_cat = json.load(files)
    cat = ['hoax', 'valid']
    all_berita = []
    unique = []
    for item in cat:
        data = " ".join(data_berita_cat[item])
        all_berita.append(data)
    kata = " ".join(all_berita)
    token = kata.split(' ')
    for item in token:
        if item:
            if item not in stopword:
                if item not in unique:
                    unique.append(item)
    unique.sort()
    if os.path.exists('../static/term_unik.json'):
        os.remove('../static/term_unik.json')
    with open('../static/term_unik.json', 'w') as file:
        json.dump(unique, file)

def weighted_berita():
    with open('../static/berita_cat.json') as files:
        data_berita_cat = json.load(files)
    categori_tokenize={}
    cat = ['hoax', 'valid']
    for item in cat:
        data = " ".join(data_berita_cat[item])
        data = data.split(' ')
        categori_tokenize[item] = data

    # print(categori_tokenize)
    with open('../static/term_unik.json') as filess:
        term_unik = json.load(filess)
    weight_cat_dict ={}
    for key in categori_tokenize:
        # print(key)
        waight_temp = []
        tes = {}
        for i in range(len(term_unik)):
            score = 0
            for item in categori_tokenize[key]:
                if term_unik[i] == item:
                    score += 1
            if score ==0:
                tes[term_unik[i]] = score
            else:tes[term_unik[i]] = 1+math.log10(score)
            waight_temp.append(score)
        weight_cat_dict[key] = tes

    if os.path.exists('../static/weighted_berita.json'):
        os.remove('../static/weighted_berita.json')
    with open('../static/weighted_berita.json', 'w') as file:
        json.dump(weight_cat_dict, file)

def conProbability():
    with open('../static/weighted_berita.json') as files:
        weight_cat_dict = json.load(files)
    with open('../static/term_unik.json') as files:
        term_unik = json.load(files)

    count_fitur = {}
    for item in weight_cat_dict:
        term_count = 0
        for val in weight_cat_dict[item]:
            term_count+=weight_cat_dict[item][val]
        count_fitur[item]= term_count

    print(count_fitur)
    conproba = {}
    for key in weight_cat_dict:
        temp = {}
        for value in weight_cat_dict[key]:
            poss_term = weight_cat_dict[key][value]
            p_kata = (poss_term + 1) / (count_fitur[key] + len(term_unik))
            temp[value] = p_kata
        conproba[key] = temp

    if os.path.exists('../static/conproba.json'):
        os.remove('../static/conproba.json')
    with open('../static/conproba.json', 'w') as file:
        json.dump(conproba, file)



# with open('../static/data.json') as file:
#     data = json.load(file)


with open('../static/data_uji.json') as f:
    data_uji = json.load(f)

with open('../static/data_latih.json') as f:
    data_latih = json.load(f)

openFile(path_offData,ratio=2/10)
berita_terkategori(data_latih)
termUnik()
weighted_berita()
conProbability()

# def testing(data):

# print(data_uji)

unclass_data_uji = []
# for item in data_uji:
#     temp={}
#     temp[item['judul']] = preprocessing(item['berita']).split()
#     unclass_data_uji.append(temp)
#
# if os.path.exists('../static/unclass_data_uji.json'):
#     os.remove('../static/unclass_data_uji.json')
# with open('../static/unclass_data_uji.json', 'w') as file:
#     json.dump(unclass_data_uji, file)

with open('../static/unclass_data_uji.json') as f:
    unclass_uji = json.load(f)

with open('../static/term_unik.json') as f:
    term_unik = json.load(f)

with open('../static/conproba.json') as f:
    conproba = json.load(f)

real_class_uji = {}
for item in data_uji:
    real_class_uji[item['judul']]=item['cat']

# print(real_class_uji)

unclass_data_uji_token = {}

for item in unclass_uji:
    for key in item:
        uniq = []
        for val in item[key]:
            if val in term_unik:
                uniq.append(val)
        unclass_data_uji_token[key]=uniq

a = {'asin':['covid','sembuh','negatif','x'],'yayan':['covid-19','x','positif','yyang']}

# print(conproba)

hasil_posterior = []
another_d=[]
for judul in unclass_data_uji_token:
    # print(judul)
    for key in conproba:
        # print(len(conproba))
        tes = []
        value = {}
        for val in conproba[key]:
            if val in unclass_data_uji_token[judul]:
                con = 1
                con*=conproba[key][val]
        another_d.append([key,con])
    hasil_posterior.append(another_d[:len(conproba)])
    for i in range(len(conproba)):
        another_d.pop()


tesa = []
tesb = []
# print(hasil_posterior)

j=0
posterior_judul={}
final_clasifikasi = {}
for judul in unclass_data_uji_token:
    for i in range(2):
        label=hasil_posterior[j][i][0]
        value=hasil_posterior[j][i][1]
        posterior_judul[label]=value
    final_clasifikasi[judul]=max(posterior_judul,key=posterior_judul.get)
    j+=1
import pandas as pd
# print(final_clasifikasi)


tes_uji_clss = final_clasifikasi
real_uji_clss = real_class_uji

hasil_salah = 0
hasil_benar = 0
for item in final_clasifikasi:
    print(item)
    print(f"hasil_klasifikasi: {final_clasifikasi[item]}"
          f"\nklasifikasi seharusnya:{real_class_uji[item]}")
    if real_class_uji[item] != final_clasifikasi[item]:
        print('TIDAK BENAR')
        hasil_salah+=1
    else:
        print('BENAR')
        hasil_benar+=1

print(f"\nHASIL KLASIFIKASI BENAR DAN SALAH:\n"
      f"Benar:{hasil_benar}\n"
      f"Salah:{hasil_salah}\n")












connn_H = 0
connn_V = 0
for key in final_clasifikasi:
    if final_clasifikasi[key]=='hoax':
        connn_H+=1
    if final_clasifikasi[key]=='valid':
        connn_V+=1

# print(connn_H)
# print(connn_V)
# print(connn_V+connn_H)
# print(tesa,tesb)


# a = 1
# b=2
# c = 100
# print(1+math.log10(a))
# print(1+math.log10(b))
# print(1+math.log10(c))
print("Program end at = ", datetime.now().time())