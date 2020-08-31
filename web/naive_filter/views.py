from django.shortcuts import render, redirect
from .models import Data
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
                    hoax = term.hoax
                    print(term.term_unik)
                    valid = term.valid
            except: print('Kata tidak ditemukan')
        print(f"hoax:{hoax}\n"
              f"valid:{valid}\n")
        print(prepro)
        hasil_klasifikasi['hoax']=hoax*probabilitas_hoax
        hasil_klasifikasi['valid']=valid*probabilitas_valid
        if max(hasil_klasifikasi.values()) == 0:
            hasil='Overflow'
        else:
            hasil=max(hasil_klasifikasi,key=hasil_klasifikasi.get)


    context = {'form': form,'hasil':hasil}

    return render(request, 'home/home.html', context)



def admin(request):
    form = DataForm()

    if request.method == "POST":
        # print('Printing Post:', request.POST)
        form = DataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_data')

    context = {'form': form}

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
