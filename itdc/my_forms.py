from asyncio.windows_events import NULL
from cProfile import label
from tkinter import Label, Widget
from unicodedata import category
from django import forms
from django.core.exceptions import ValidationError
from .models import *
from django.forms import ModelForm, widgets

# Model Form for bootstrap
class BootstrapModelForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

# Form for bootstrap
class BootstrapForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

# Model Form for cluster
class ClusterForm(BootstrapModelForm):
    location = forms.ModelChoiceField(queryset=Location.objects.all(),to_field_name='name')
    is_container = forms.ChoiceField(label='Is_Container',choices=[(1,'Yes'),(0,'No')])
    class Meta:
        model = Asset
        fields = ('location','name','is_container','is_active','comment')
        widgets = {
            'comment':forms.Textarea(attrs={'rows':1}),
        }

# Model Form for physical server
class PMForm(BootstrapModelForm):
    location = forms.ModelChoiceField(queryset=Location.objects.all(),to_field_name='name')
    container = forms.ModelChoiceField(queryset=Asset.objects.filter(is_container=True,is_active=True),required=False)
    class Meta:
        model = Asset
        fields = ('location','model','sn','name','container','os','cpu','memory','hdd','is_active','is_poweron','is_container','purchase_date','expire_date','price','vendor','comment')
        widgets = {
            'comment':forms.Textarea(attrs={'rows':1}),
            'purchase_date':forms.NumberInput(attrs={'type':'date'}),
            'expire_date':forms.NumberInput(attrs={'type':'date'}),
        }


# Model Form for storage
class StorageForm(BootstrapModelForm):
    location = forms.ModelChoiceField(queryset=Location.objects.all(),to_field_name='name')
    container = forms.ModelChoiceField(queryset=Asset.objects.filter(is_container=True,is_active=True),required=False)
    class Meta:
        model = Asset
        fields = ('location','model','sn','name','container','is_active','is_poweron','hdd','purchase_date','expire_date','price','vendor','comment')
        widgets = {
            'comment':forms.Textarea(attrs={'rows':1}),
            'purchase_date':forms.NumberInput(attrs={'type':'date'}),
            'expire_date':forms.NumberInput(attrs={'type':'date'}),
        }


# Model Form for switch
class SwitchForm(BootstrapModelForm):
    location = forms.ModelChoiceField(queryset=Location.objects.all(),to_field_name='name')
    class Meta:
        model = Asset
        fields = ('location','model','sn','name','is_active','is_poweron','purchase_date','expire_date','price','vendor','comment')
        widgets = {
            'comment':forms.Textarea(attrs={'rows':1}),
            'purchase_date':forms.NumberInput(attrs={'type':'date'}),
            'expire_date':forms.NumberInput(attrs={'type':'date'}),
        }
  

# Model Form for virtual server
class VMForm(BootstrapModelForm):
    location = forms.ModelChoiceField(queryset=Location.objects.all(),to_field_name='name')
    container = forms.ModelChoiceField(queryset=Asset.objects.filter(is_container=True,is_active=True),required=False)
    class Meta:
        model = Asset
        fields = ('location','name','container','os','cpu','memory','hdd','is_active','is_poweron','comment')
        widgets = {
            'comment':forms.Textarea(attrs={'rows':1}),
        }


# Model Form for other assets
class OtherForm(BootstrapModelForm):
    location = forms.ModelChoiceField(queryset=Location.objects.all(),to_field_name='name')
    class Meta:
        model = Asset
        fields = ('location','model','sn','name','is_active','is_poweron','comment')
        widgets = {
            'comment':forms.Textarea(attrs={'rows':1}),
        }

# Model Form to add comment
class AssetCommentForm(BootstrapModelForm):
    class Meta:
        model = AssetComment
        fields = ('comment',)
        widgets = {
            'comment':forms.Textarea(attrs={'rows':2}),
        }

# Model Form for software
class SoftwareForm(BootstrapModelForm):
    class Meta:
        model = Software
        fields = ('name','softwarekey','quantity','comment')
        widgets = {
            'comment':forms.Textarea(attrs={'rows':1}),
        }

# Model Form for IP
class IpForm(BootstrapModelForm):
    class Meta:
        model = IpAddress
        fields = ('location','address','comment')
        widgets = {
            'comment':forms.Textarea(attrs={'rows':1}),
        }

# Form to add IP
class IpAddForm(BootstrapForm):    
    ip_start = forms.GenericIPAddressField(label='IP Start',required=True)
    ip_end = forms.GenericIPAddressField(label='IP End',required=True)
    location = forms.CharField(label='Location',max_length=50,required=True)
    comment = forms.CharField(label='Comment',required=False)

# Model Form for network port
class PortForm(BootstrapModelForm):
    class Meta:
        model = NetworkPort
        fields = ('port_number','connect_to','comment')
        widgets = {
            'comment':forms.Textarea(attrs={'rows':1}),
        }

# Form to add networkport
class PortAddForm(BootstrapForm):    
    port_start = forms.IntegerField(label='Port Start')
    port_end = forms.IntegerField(label='Port End')


# Form for asset list filter
class AssetFilterForm(forms.Form):
    category_choice = [('','Category'),('PM','PM'),('VM','VM'),('Cluster','Cluster'),('Storage','Storage'),('Switch','Switch'),('UPS','UPS'),('Tape','Tape')]
    category = forms.ChoiceField(label='Category',choices=category_choice)
    location = forms.ModelChoiceField(label='Location',queryset=Location.objects.all(),to_field_name='name',empty_label='Location',required=False)
    is_active = forms.ChoiceField(label='Is_Active',choices=[('','Active Status'),(1,'Active'),(0,'Inactive')])
    is_poweron = forms.ChoiceField(label='Is_PowerOn',choices=[('','Power Status'),(1,'Power On'),(0,'Power Off')])
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # Add class for fields
        for name,field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control filters'
            else:
                field.widget.attrs['class'] = 'form-control filters'

    