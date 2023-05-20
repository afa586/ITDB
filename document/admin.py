from django.contrib import admin
from .models import Document

# Register your models here.
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name','folder','lastwrite')
    # fields = ('name','folder','lastwrite')
    search_fields = ('name','folder')

admin.site.register(Document,DocumentAdmin)





