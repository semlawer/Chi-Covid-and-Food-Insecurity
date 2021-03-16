# Generated by Django 3.1.7 on 2021-03-14 22:32

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CovidFood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objectid', models.FloatField()),
                ('shape_area', models.FloatField()),
                ('shape_len', models.FloatField()),
                ('zip', models.BigIntegerField()),
                ('fs_ratio', models.FloatField()),
                ('pr_fs_rati', models.FloatField()),
                ('death_rate', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'Covid_Food',
            },
        ),
        migrations.CreateModel(
            name='FoodBanks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=80)),
                ('name', models.CharField(max_length=80)),
                ('zip_code', models.CharField(max_length=80)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'Food Banks',
            },
        ),
    ]