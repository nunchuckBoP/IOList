# Generated by Django 3.2.9 on 2021-11-15 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IOList', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='busdevice',
            name='description_1',
            field=models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 1'),
        ),
        migrations.AddField(
            model_name='busdevice',
            name='description_2',
            field=models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 2'),
        ),
        migrations.AddField(
            model_name='busdevice',
            name='description_3',
            field=models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 3'),
        ),
        migrations.AddField(
            model_name='busdevice',
            name='description_4',
            field=models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 4'),
        ),
        migrations.AlterField(
            model_name='point',
            name='description_1',
            field=models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 1'),
        ),
        migrations.AlterField(
            model_name='point',
            name='description_2',
            field=models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 2'),
        ),
        migrations.AlterField(
            model_name='point',
            name='description_3',
            field=models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 3'),
        ),
        migrations.AlterField(
            model_name='point',
            name='description_4',
            field=models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 4'),
        ),
    ]
