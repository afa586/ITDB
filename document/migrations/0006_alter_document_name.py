# Generated by Django 4.1.2 on 2022-11-16 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0005_rename_indexteime_document_indextime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Name'),
        ),
    ]