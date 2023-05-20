from django.db import models

# Create your models here.

#Model for document form
class Document(models.Model):
    name = models.CharField('Name',max_length=200)
    rootfolder = models.CharField('Root Folder',max_length=200,null=True,blank=True)
    folder = models.TextField('Folder')
    lastwrite = models.DateTimeField('Last Write')
    indextime = models.DateTimeField('Index Time',auto_now_add=True)
    def __str__(self):
        return self.name

