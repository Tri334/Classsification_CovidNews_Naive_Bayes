from django.shortcuts import render, redirect
from .models import Data
from .form import DataForm
import json
from django.http import JsonResponse
import os
# Create your views here.


def index(request):
    return render(request, 'home/index.html')


def home(request):
    return render(request, 'home/home.html')


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
