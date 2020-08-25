import json
from .models import *
from .resources import *
import os


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

    for label in data:
        print(label)
        for kata in data[label]:
            nilai = data[label][kata]
            print(kata)
            print(nilai)
            if TermUnikValue.objects.filter(term_unik=kata).exists():
                TermUnikValue.objects.filter(term_unik=kata).update(valid=nilai)
            else:TermUnikValue.objects.create(term_unik=kata,valid=999,hoax=nilai)



