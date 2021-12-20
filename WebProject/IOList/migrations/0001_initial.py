# Generated by Django 3.2.9 on 2021-12-20 19:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chassis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=256, verbose_name='Make / Manufacturer')),
                ('part_number', models.CharField(max_length=256, verbose_name='Part / Catalog Number')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('name', models.CharField(max_length=26)),
                ('address', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ValveBank',
            fields=[
                ('chassis_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='IOList.chassis')),
                ('data_format', models.IntegerField(choices=[(4, 'SINT DATA'), (8, 'INT DATA')])),
                ('valve_count', models.IntegerField()),
                ('address_template', models.CharField(blank=True, max_length=82, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('IOList.chassis',),
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=100, verbose_name='Short Name')),
                ('street', models.CharField(blank=True, max_length=140, null=True, verbose_name='Address Line 1')),
                ('line2', models.CharField(blank=True, max_length=140, null=True, verbose_name='Address Line 2')),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=5, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=25, null=True, verbose_name='Zip Code')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IOList.customer')),
            ],
            options={
                'unique_together': {('customer', 'short_name')},
            },
        ),
        migrations.CreateModel(
            name='IOList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=82, verbose_name='IO List Name')),
                ('controller', models.CharField(blank=True, max_length=256, null=True, verbose_name='Controller Name')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='IOList_Created_By', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='IOList_Modified_By', to=settings.AUTH_USER_MODEL)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IOList.plant')),
            ],
            options={
                'unique_together': {('plant', 'name')},
            },
        ),
        migrations.AddField(
            model_name='chassis',
            name='io_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IOList.iolist'),
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=256, verbose_name='Make / Manufacturer')),
                ('part_number', models.CharField(max_length=256, verbose_name='Part / Catalog Number')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('slot', models.IntegerField()),
                ('address_template', models.CharField(blank=True, max_length=256, null=True)),
                ('chassis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IOList.chassis')),
            ],
            options={
                'unique_together': {('chassis', 'slot')},
            },
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('type', models.CharField(choices=[('DI', 'Discrete Input'), ('DO', 'Discrete Output'), ('AI', 'Analog Input'), ('AO', 'Analog Output'), ('RTD', 'RTD Input'), ('TC', 'Thermocouple, Input'), ('HSC', 'High Speed Count Input')], max_length=6)),
                ('tag', models.CharField(max_length=26)),
                ('description_1', models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 1')),
                ('description_2', models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 2')),
                ('description_3', models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 3')),
                ('description_4', models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 4')),
                ('user_address', models.CharField(blank=True, max_length=82, null=True, verbose_name='User Specified Address')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IOList.card')),
            ],
            options={
                'unique_together': {('card', 'number')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='chassis',
            unique_together={('io_list', 'address')},
        ),
        migrations.CreateModel(
            name='BusDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=256, verbose_name='Make / Manufacturer')),
                ('part_number', models.CharField(max_length=256, verbose_name='Part / Catalog Number')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('address', models.CharField(max_length=26)),
                ('tag', models.CharField(max_length=26)),
                ('description_1', models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 1')),
                ('description_2', models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 2')),
                ('description_3', models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 3')),
                ('description_4', models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 4')),
                ('io_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IOList.iolist')),
            ],
            options={
                'unique_together': {('io_list', 'tag')},
            },
        ),
        migrations.CreateModel(
            name='Solenoid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('tag', models.CharField(max_length=26)),
                ('description_1', models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 1')),
                ('description_2', models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 2')),
                ('description_3', models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 3')),
                ('description_4', models.CharField(blank=True, max_length=26, null=True, verbose_name='Desc 4')),
                ('user_address', models.CharField(blank=True, max_length=82, null=True, verbose_name='User Specified Address')),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IOList.valvebank')),
            ],
            options={
                'unique_together': {('bank', 'number')},
            },
        ),
    ]
