# Generated by Django 3.2.9 on 2021-12-20 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IOList', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='name',
            field=models.CharField(default='CP400S01', max_length=140),
            preserve_default=False,
        ),
    ]
