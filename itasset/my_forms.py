from asyncio.windows_events import NULL
from cProfile import label
from tkinter import Label, Widget
from unicodedata import category
from django import forms
from django.core.exceptions import ValidationError
from .models import *
from django.forms import ModelForm, widgets


# Model Form for asset
class AssetForm(ModelForm):
    company = forms.ModelChoiceField(label='Company',queryset=Company.objects.all().order_by('name'),to_field_name='name')
    category = forms.ModelChoiceField(label='Category',queryset=AssetCategory.objects.all().order_by('name'),to_field_name='name')
    office = forms.ModelChoiceField(label='Office',queryset=OfficeVersion.objects.all().order_by('name'),to_field_name='name',required=False)
    initial_os = forms.ModelChoiceField(label='Initial OS',queryset=OperationSystem.objects.all().order_by('name'),to_field_name='name',required=False)
    os = forms.ModelChoiceField(label='OS',queryset=OperationSystem.objects.all().order_by('name'),to_field_name='name',required=False)
    memory = forms.ModelChoiceField(label='Memory',queryset=Memory.objects.all().order_by('name'),to_field_name='name',required=False)
    hdd = forms.ModelChoiceField(label='HDD',queryset=HardDisk.objects.all().order_by('name'),to_field_name='name',required=False)
    class Meta:
        model = Asset
        fields = ('company','category','model','sn','name','purchase_date','warranty','price','initial_os','os','office','cpu','memory','hdd','vendor','comment')
        widgets = {
            'purchase_date': forms.NumberInput(attrs={'type':'date'}),
            'comment': forms.Textarea(attrs={'rows':1})
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)        
        for name,field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
          

# Model Form for user
class UserForm(ModelForm):
    company = forms.ModelChoiceField(label='Company',queryset=Company.objects.all().order_by('name'),to_field_name='name')
    department = forms.ModelChoiceField(label='Department',queryset=Department.objects.all().order_by('name'),to_field_name='name')
    location = forms.ModelChoiceField(label='Location',queryset=Location.objects.all().order_by('name'),to_field_name='name')
    class Meta:
        model = User
        fields = ('account','name','company','department','location','comment')
        widgets = {
            'comment': forms.Textarea(attrs={'rows':1})
        }
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)     
        for name,field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

# Form for asset list filter
class AssetFilterForm(forms.Form):
    company = forms.ModelChoiceField(label='Company',queryset=Company.objects.all(),to_field_name='name',empty_label='All Company')
    category = forms.ModelChoiceField(label='Category',queryset=AssetCategory.objects.all(),to_field_name='name',empty_label='All Category')
    status = forms.ModelChoiceField(label='Status',queryset=AssetStatus.objects.all(),empty_label='All Status')
    def __init__(self,*args,**kwargs):
        super(AssetFilterForm,self).__init__(*args,**kwargs)       
        for name,field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control filters'
            else:
                field.widget.attrs['class'] = 'form-control filters'


# Form for user list filter
class UserFilterForm(forms.Form):
    company = forms.ModelChoiceField(label='Company',queryset=Company.objects.all(),to_field_name='name',empty_label='All Company')
    is_active = forms.ChoiceField(label='Status',choices=[('','All Status'),(1,'Normal'),(0,'Resigned')])
    def __init__(self,*args,**kwargs):
        super(UserFilterForm,self).__init__(*args,**kwargs)      
        for name,field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control filters'
            else:
                field.widget.attrs['class'] = 'form-control filters'

# Form for asset list custom filter
class AssetCustomFilterForm(forms.Form):
    company = forms.ModelChoiceField(label='Company',queryset=Company.objects.all(),to_field_name='name',empty_label='All Company')
    category = forms.ModelChoiceField(label='Category',queryset=AssetCategory.objects.all(),to_field_name='name',empty_label='All Category')
    status = forms.ModelChoiceField(label='Status',queryset=AssetStatus.objects.all(),empty_label='All Status')
    office = forms.ModelChoiceField(label='Office',queryset=OfficeVersion.objects.all(),to_field_name='name',empty_label='All Office')
    os = forms.ModelChoiceField(label='OS',queryset=OperationSystem.objects.all(),to_field_name='name',empty_label='All OS')
    def __init__(self,*args,**kwargs):
        super(AssetCustomFilterForm,self).__init__(*args,**kwargs)
        # Add class for fields
        for name,field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control filters'
            else:
                field.widget.attrs['class'] = 'form-control filters'

# Form for tanium
class TaniumForm(ModelForm):
    class Meta:
        model = Tanium
        fields = '__all__'
        exclude = ['create_time']
