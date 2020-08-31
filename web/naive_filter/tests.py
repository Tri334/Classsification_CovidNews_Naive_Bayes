import json
from .models import *
from .resources import *
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
from datetime import datetime

factory = StemmerFactory()
stemmer = factory.create_stemmer()

subs2 = '\s *\w\. |\(|\)|:|, |\.\n|”|“|…|\.  |&|\*|\?|"|- | -'
subs3 ='\. |, |\/\n'
substwith= '\n+|\s +'

print("Program start at = ", datetime.now().time())

def sendoffData():
    with open('static/data_latih.json') as f:
        ff = json.loads(f.read())

    Data.objects.all().delete()
    for item in ff:
        Data.objects.create(judul=item['judul'],cat=item['cat'], berita=item['berita'])

def sendtermUnik():
    with open('static/conproba.json') as data:
        data = json.loads(data.read())

    TermUnikValue.objects.all().delete()

    for item in data:
        for key in data[item]:
            temp_nilai = data[item][key]
            if item=='hoax':
                TermUnikValue.objects.create(term_unik=key,hoax=temp_nilai,valid = 999)
            elif item=='valid':
                TermUnikValue.objects.filter(term_unik=key).update(valid=temp_nilai)

def preprocessing(berita):
    cleaning_words = re.sub(subs2, " ", berita)
    cleaning_words = re.sub(subs3, " ", cleaning_words)
    cleaning_words = re.sub(substwith, " ", cleaning_words)
    clean = cleaning_words.lower()
    tokenize = clean.split()
    token = " ".join(tokenize)
    return stemmer.stem(token)



print("Program start at = ", datetime.now().time())
