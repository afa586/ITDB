# Generated by Django 4.0.8 on 2023-03-08 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itasset', '0014_asset_initial_os_alter_user_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Asset Name'),
        ),
        migrations.AlterField(
            model_name='tanium',
            name='name',
            field=models.CharField(max_length=300, verbose_name='Computer Name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='account',
            field=models.CharField(max_length=20, unique=True, verbose_name='Account'),
        ),
    ]