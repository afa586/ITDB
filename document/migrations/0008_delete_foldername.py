# Generated by Django 4.1.2 on 2022-11-21 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0007_document_rootfolder'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FolderName',
        ),
    ]
