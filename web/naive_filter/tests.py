import json
from .models import *
from .resources import *
import os

data = Data
term = TermUnikValue

def sendoffData(data):
    with open('static/data_latih.json') as f:
        ff = json.loads(f.read())

    data.objects.all().delete()
    for item in ff:
        data.objects.create(judul=item['judul'],cat=item['cat'], berita=item['berita'])

def sendtermUnik(term):
    with open('static/conproba.json') as data:
        data = json.loads(data.read())

    term.objects.all().delete()
    for item in data:
        term.objects.create(term_unik=item,valid=data[item]['valid'],hoax=data[item]['hoax'])


with open('static/conproba.json') as data:
    data = json.loads(data.read())

