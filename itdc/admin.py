from django.contrib import admin
from itdc.models import Location,Asset
from django.forms import ModelChoiceField

# Register your models here.

@admin.register(Location)
class CommonAdmin(admin.ModelAdmin):
    list_display = ('id','name','comment')
    # fields = ('name','comment')
    search_fields = ('name',)

@admin.register(Asset)
class ElementAdmin(admin.ModelAdmin):
    list_display = ('location','category','model','sn','name','container','os','cpu','memory','hdd','is_active','is_container','purchase_date','expire_date','price','vendor','comment')
    # fields = ('location','model','sn','name','os','cpu','memory','hdd','is_active','is_container','purchase_date','expire_date','price','vendor','comment')
    search_fields = ('name',)
    

