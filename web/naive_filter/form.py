from django.forms import ModelForm
from  .models import Data
from django import forms

class DataForm(ModelForm):
    class Meta:
        model = Data
        fields = '__all__'

class InputForm(forms.Form):
    berita = forms.CharField(widget=forms.Textarea,required=True)