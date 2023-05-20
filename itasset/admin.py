from django.contrib import admin
from .models import Company,Department,Location,AssetCategory,AssetStatus,OfficeVersion,OperationSystem,Memory,HardDisk,Asset,User

# Modify admin site info
admin.sites.AdminSite.site_header = 'Snap-on IT Operation System'
admin.sites.AdminSite.site_title = 'Snap-on IT Operation System'


# Register your models here.

@admin.register(Company,Department,Location,AssetCategory,AssetStatus,OfficeVersion,OperationSystem,Memory,HardDisk)
class CommonAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    search_fields = ('name',)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('company','category','model','sn','name','status','purchase_date','price','os','office','cpu','memory','hdd','vendor','comment')
    search_fields = ('name',)

@admin.register(User)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('account','name','company','department','location','comment')
    search_fields = ('name',)