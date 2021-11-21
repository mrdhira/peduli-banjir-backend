from django.conf import settings
from django.db import models
from app.user.models import User
from app.location.models import Location
from .managers import ForumPostManager, ForumThreadManager


class Status(models.IntegerChoices):
    INACTIVE = 0, "InActive"
    ACTIVE = 1, "Active"


# Create your models here.
class ForumPost(models.Model):
    class ForumPostCategory(models.IntegerChoices):
        DEFAULT = 1, "Default"
        REPORT = 2, "Report"

    user_creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="forum_post",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="forum_post",
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.IntegerField(
        choices=ForumPostCategory.choices,
        default=ForumPostCategory.DEFAULT,
    )
    total_like = models.IntegerField(default=0, editable=False)
    total_comment = models.IntegerField(default=0, editable=False)
    total_view = models.IntegerField(default=0, editable=False)
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    object = ForumPostManager()

    def __str__(self) -> str:
        return f"{self.user_creator.full_name} - {self.title}"

    class Meta:
        db_table = "forum_post"


class ForumPostLike(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="forum_post_like",
    )
    post = models.ForeignKey(
        ForumPost,
        on_delete=models.CASCADE,
        related_name="forum_post_like",
    )

    class Meta:
        db_table = "forum_post_like"


class ForumPostPicture(models.Model):
    post = models.ForeignKey(
        ForumPost, on_delete=models.CASCADE, related_name="forum_post_picture"
    )
    picture = models.ImageField(upload_to="forum/picture/")
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    def get_picture(self):
        if self.picture:
            if settings.ENV == "local":
                return "http://127.0.0.1:3000" + self.picture.url
            else:
                return self.picture.url
        return ""

    class Meta:
        db_table = "forum_post_picture"


class ForumThread(models.Model):
    user_creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="forum_thread",
    )
    post = models.ForeignKey(
        ForumPost,
        on_delete=models.CASCADE,
        related_name="thread",
    )
    parent_thread = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="sub_thread",
        blank=True,
        null=True,
    )
    content = models.TextField()
    total_like = models.IntegerField(default=0, editable=False)
    total_comment = models.IntegerField(default=0, editable=False)
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    object = ForumThreadManager()

    class Meta:
        db_table = "forum_thread"


class ForumThreadLike(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="forum_thread_like",
    )
    thread = models.ForeignKey(
        ForumThread,
        on_delete=models.CASCADE,
        related_name="forum_thread_like",
    )

    class Meta:
        db_table = "forum_thread_like"
