# Generated by Django 3.2.9 on 2021-11-21 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0003_auto_20211121_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='weathercurrent',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='weathercurrent',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='weatherdesc',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='weatherdesc',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='weatherforecast',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='weatherforecast',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
