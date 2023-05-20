# Generated by Django 4.1.1 on 2022-11-15 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itasset', '0008_delete_assetmodel_asset_warranty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tanium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Computer Name')),
                ('lastsee', models.CharField(blank=True, max_length=150, null=True, verbose_name='Last See')),
                ('os_install_date', models.CharField(blank=True, max_length=150, null=True, verbose_name='OS Install Date')),
                ('os', models.CharField(blank=True, max_length=150, null=True, verbose_name='OS')),
                ('username', models.CharField(blank=True, max_length=150, null=True, verbose_name='User Name')),
                ('model', models.CharField(blank=True, max_length=150, null=True, verbose_name='Model')),
                ('last_reboot', models.CharField(blank=True, max_length=150, null=True, verbose_name='Last Reboot')),
            ],
        ),
        migrations.AlterField(
            model_name='asset',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='userhistory',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Comment'),
        ),
    ]
