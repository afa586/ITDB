# Generated by Django 4.1.2 on 2022-10-19 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0002_alter_document_lastwrite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='lastwrite',
            field=models.DateTimeField(verbose_name='Last Write'),
        ),
    ]