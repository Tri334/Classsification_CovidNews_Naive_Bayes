from django.shortcuts import render, redirect
from fractions import Fraction
from .tests import *
from .form import *
import json
from django.http import JsonResponse
import os
# Create your views here.


def index(request):
    return render(request, 'home/index.html')


def home(request):
    form = InputForm()
    hasil =''
    prepro=''
    if request.method == "POST":
        # print('Printing Post:', request.POST)
        # form = InputForm(request.POST)
        # if form.is_valid():
        hasil = request.POST['berita']

        prepro = preprocessing(hasil).split()
        hasil_klasifikasi = {}
        jumlah_data = Data.objects.all()
        jumlah_data_hoax = Data.objects.filter(cat='hoax')
        probabilitas_hoax=(jumlah_data_hoax.count())/jumlah_data.count()
        probabilitas_valid=(jumlah_data.count()-jumlah_data_hoax.count())/jumlah_data.count()
        hoax = 1
        valid = 1
        tm = []
        for item in prepro:
            try:
                if TermUnikValue.objects.get(term_unik=item):
                    term = TermUnikValue.objects.get(term_unik=item)
                    hoax = Fraction(term.hoax)
                    print(term.term_unik)
                    valid = Fraction(term.valid)
            except: print('Kata tidak ditemukan')
        print(f"hoax:{hoax}\n"
              f"valid:{valid}\n")
        print(prepro)
        hasil_klasifikasi['hoax']=hoax*probabilitas_hoax
        hasil_klasifikasi['valid']=valid*probabilitas_valid
        if max(hasil_klasifikasi.values()) == 0:
            hasil='Tidak Diketahui'
        else:
            hasil=max(hasil_klasifikasi,key=hasil_klasifikasi.get)
    print(hasil)


    context = {'form': form,'hasil':hasil}

    return render(request, 'home/home.html', context)



def admin(request):
    form = DataForm()
    duplikat = 'Aman'
    status = ''
    data_hoax = Data.objects.filter(cat='hoax').count()
    data_valid = Data.objects.filter(cat='valid').count()

    if request.method == "POST":
        post = request.POST
        juduls = post['judul']
        try:
            if Data.objects.get(judul=juduls):
                duplikat = 'Berita Duplikat'
                status = 'notok'
            else:
                duplikat = 'Aman'
                status = 'ok'
        except:
            status = 'ok'

        if status == 'ok' and duplikat == 'Aman':
            form = DataForm(request.POST)
            if form.is_valid():
                print('form di save',request.POST)
                # form.save()
                return redirect('add_data')

    context = {'form': form, 'duplikat': duplikat, 'datahoax': data_hoax, 'datavalid': data_valid}

    return render(request, 'home/admin_page.html', context)


def send_json(request):
    with open('static/data.json') as f:
        ff = json.loads(f.read())

    return JsonResponse(ff, safe=False)


def dumpData(request):
    data = Data.objects.all()
    total_data = data.count()

    context = {'data': total_data}
    return render(request, 'offDB/off.html', context)
