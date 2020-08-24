from django.db import models
import json

# Create your models here.

class Data(models.Model):
    category = (('hoax', 'hoax'), ('valid', 'valid'))
    judul = models.CharField(blank=False, null=False, max_length=150)
    cat = models.CharField(blank=False, null=False,max_length=50, choices=category)
    berita = models.TextField(blank=False, null=False)


class TermUnikValue(models.Model):
    term_unik = models.CharField(blank=False, null=False, max_length=150)
    valid = models.FloatField(blank=False, null=False)
    hoax = models.FloatField(blank=False, null=False)


