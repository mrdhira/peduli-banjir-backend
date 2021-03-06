# Generated by Django 3.2.9 on 2021-11-21 01:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('forum', '0001_initial'),
        ('location', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='forumthreadlike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_thread_like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='forumthread',
            name='parent_thread',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_thread', to='forum.forumthread'),
        ),
        migrations.AddField(
            model_name='forumthread',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thread', to='forum.forumpost'),
        ),
        migrations.AddField(
            model_name='forumthread',
            name='user_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_thread', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='forumpostpicture',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_post_picture', to='forum.forumpost'),
        ),
        migrations.AddField(
            model_name='forumpostlike',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_post_like', to='forum.forumpost'),
        ),
        migrations.AddField(
            model_name='forumpostlike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_post_like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='forumpost',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_post', to='location.location'),
        ),
        migrations.AddField(
            model_name='forumpost',
            name='user_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_post', to=settings.AUTH_USER_MODEL),
        ),
    ]
