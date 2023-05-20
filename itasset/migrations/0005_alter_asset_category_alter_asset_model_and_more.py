# Generated by Django 4.1.1 on 2022-10-27 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itasset', '0004_assethistory_action_alter_asset_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='category',
            field=models.CharField(max_length=20, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='model',
            field=models.CharField(max_length=50, verbose_name='Model'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.CharField(max_length=20, verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.CharField(max_length=20, verbose_name='Department'),
        ),
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.CharField(max_length=20, verbose_name='Location'),
        ),
    ]
