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
    for item in data:
        TermUnikValue.objects.create(term_unik=item,valid=data[item]['valid'],hoax=data[item]['hoax'])


sendtermUnik()

