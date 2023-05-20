# Generated by Django 4.1.2 on 2022-10-26 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('itasset', '0002_rename_osversion_operationsystem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='sn',
            field=models.CharField(max_length=20, unique=True, verbose_name='Serial Number'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='status',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='itasset.assetstatus', verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='account',
            field=models.CharField(max_length=20, unique=True, verbose_name='Acount'),
        ),
    ]
