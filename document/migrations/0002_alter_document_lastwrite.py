# Generated by Django 4.1.2 on 2022-10-19 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='lastwrite',
            field=models.CharField(max_length=100, verbose_name='Last Write'),
        ),
    ]
