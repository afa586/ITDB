from cProfile import label
from tkinter import Label, Widget
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, widgets
from document.models import *
from django.db.models import Count 

# Model form for document
class documentForm(ModelForm):
    class Meta:
        model = Document
        fields = ('name','folder','lastwrite')


# Form to filter document
class DocumentFilterForm(forms.Form):    
    year = forms.ChoiceField(label='Year',choices=[('','All year')])
    folder = forms.ChoiceField(label='Folder',choices=[('','All rootfolder')])
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control filters'
            else:
                field.widget.attrs['class'] = 'form-control filters'

# Form to search document
class CustomSearchForm(forms.Form):
    name = forms.CharField(label='File Name',required=False)
    folder = forms.CharField(label='Folder',required=False)
    year = forms.CharField(label='Year',required=False)    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # Add class for fields
        for name,field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control filters'                
            else:
                field.widget.attrs['class'] = 'form-control filters'
            field.widget.attrs['placeholder'] = field.label
