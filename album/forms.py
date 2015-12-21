from django import forms
from album.models import Image
from django.contrib import admin

class UploadFileForm(forms.ModelForm):


    class Meta:
        model = Image
        fields = '__all__'
        exclude = ('user',)
