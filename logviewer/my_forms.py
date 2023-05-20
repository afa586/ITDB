from django import forms
from logviewer.models import *
from django.forms import ModelForm, widgets

#Form to filter windows event logs
class NetEventFilter(forms.Form):
    date_from = forms.DateField(label='From', widget=forms.NumberInput(attrs={'type':'date'}))
    date_to = forms.DateField(label='To', widget=forms.NumberInput(attrs={'type':'date'}))
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)      
        for name,field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control filters'
            else:
                field.widget.attrs['class'] = 'form-control filters'
    


# Form to filter windows event solution
status_choices = NetEventSolution.status_choices
fix_by_choices = (('','Fix By'),('Network','Network'),('APP','APP'))
class NetEventSolutionFilter(forms.Form):
    status = forms.ChoiceField(label='Status',choices=status_choices)
    fix_by = forms.ChoiceField(label='Fix By',choices=fix_by_choices)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # Add class for fields
        for name,field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control filters'
            else:
                field.widget.attrs['class'] = 'form-control filters'


# Model Form for Net Event solution
class NetEventSolutionForm(ModelForm):
    class Meta:
        model = NetEventSolution
        fields = ('solution_id','date','event_id','source','error_desc','os','fix_by')
        widgets = {
            'date': forms.NumberInput(attrs={'type':'date'}),
            'error_desc': forms.Textarea(attrs={'rows':4})
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)        
        for name,field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

# Model Form for Net Event solution(for cause provider)
class NetEventSolutionCauseForm(ModelForm):
    class Meta:
        model = NetEventSolution
        fields = ('severity','action','cause')
        widgets = {
            'cause': forms.Textarea(attrs={'rows':4}),
            'action': forms.Textarea(attrs={'rows':1}),
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)        
        for name,field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'