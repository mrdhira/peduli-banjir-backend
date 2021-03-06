# Generated by Django 3.2.9 on 2021-11-21 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='weathercurrent',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='weatherforecast',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='clouds',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='dew_point',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='dt',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='feels_like',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='feels_like_day',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='feels_like_eve',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='feels_like_morn',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='feels_like_night',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='humidity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='moon_phase',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='moonrise',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='moonset',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='pop',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='precipitation',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='pressure',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='rain',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='rain_1h',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='sunrise',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='sunset',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='temp',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='temp_day',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='temp_eve',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='temp_max',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='temp_min',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='temp_morn',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='temp_night',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='timezone',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='timezone_offset',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='type',
            field=models.IntegerField(blank=True, choices=[(1, 'Current'), (2, 'Minutely'), (3, 'Hourly'), (4, 'Daily')], null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='uvi',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='visibility',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='wind_deg',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='wind_gust',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='wind_speed',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
