# Generated by Django 3.2.9 on 2021-11-21 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='forumpost',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='forumthread',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='forumpost',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='forumpost',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='forumpostpicture',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='forumpostpicture',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='forumthread',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='forumthread',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
