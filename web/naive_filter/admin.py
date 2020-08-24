from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(Data)
class DataAdmin(ImportExportModelAdmin):
    list_display = ('judul', 'cat', 'berita')


@admin.register(TermUnikValue)
class Term(ImportExportModelAdmin):
    list_display = ('term_unik','hoax','valid')


