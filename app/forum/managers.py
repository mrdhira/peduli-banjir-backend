import logging
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Manager, Exists, F
from app.location.models import Location


logger = logging.getLogger(__name__)


class ForumPostManager(Manager):
    def get_post(self, fields):
        from .models import Status, ForumPostLike

        user = fields.get("user")
        page = fields.get("page", 0)
        limit = fields.get("limit", 10)
        order_by = fields.get("order_by", "-created_at")
        category = fields.get("category", None)
        latitude = fields.get("latitude", None)
        longtitude = fields.get("longtitude", None)

        offset = page * limit

        post = self.select_related("user_creator").filter(status=Status.ACTIVE)

        if category:
            post = post.filter(category=category)

        if not user.is_anonymous:
            post.annotate(
                post_like_exist=Exists(
                    ForumPostLike.objects.filter(user=user),
                )
            )

        return post.order_by(order_by)[offset : offset + limit]

    def get_post_detail(self, fields, post_id):
        from .models import Status, ForumPostLike

        user = fields.get("user")

        post = (
            self.select_related("user_creator")
            .prefetch_related(
                "forum_post_like",
                "forum_post_picture",
                "forum_thread",
                "forum_thread__sub_thread",
            )
            .filter(
                id=post_id,
                status=Status.ACTIVE,
                forum_post_picture__status=Status.ACTIVE,
            )
            .first()
        )

        if not post:
            raise ObjectDoesNotExist

        if not user.is_anonymous:
            post.annotate(
                post_like_exist=Exists(
                    ForumPostLike.objects.filter(user=user),
                )
            )

        return post

    def create_post(self, fields):
        user = fields.get("user")
        latitude = fields.get("latitude")
        longtitude = fields.get("longtitude")
        title = fields.get("title")
        content = fields.get("content")
        category = fields.get("category")

        with transaction.atomic():
            location = Location.objects.get_location(latitude, longtitude)

            post = self.create(
                user_creator=user,
                location=location,
                title=title,
                content=content,
                category=category,
            )

            # TODO: Insert picture to forum_post_picture

            return post

    def action_like(self, fields, post_id):
        user = fields.get("user")

        from .models import ForumPostLike

        with transaction.atomic():
            post = self.filter(id=post_id).first()

            if not post:
                raise ObjectDoesNotExist

            post_like = ForumPostLike.objects.filter(user, post).first()

            if not post_like:
                post_like = self.create(user, post)
                self.incr_like(post.id)
            else:
                post_like.delete()
                self.decr_like(post.id)

        return

    def incr_like(self, post_id):
        return self.filter(id=post_id).update(total_like=F("total_like") + 1)

    def decr_like(self, post_id):
        return self.filter(id=post_id).update(total_like=F("total_like") - 1)

    def incr_comment(self, post_id):
        return self.filter(id=post_id).update(total_comment=F("total_comment") + 1)

    def decr_comment(self, post_id):
        return self.filter(id=post_id).update(total_comment=F("total_comment") - 1)


class ForumThreadManager(Manager):
    def create_thread(self, fields, post_id):
        from .models import ForumPost

        user = fields.get("user")
        parent_thread_id = fields.get("parent_thread_id")
        content = fields.get("content")

        with transaction.atomic():
            # Get Post
            post = ForumPost.objects.filter(id=post_id).first()

            if not post:
                raise ObjectDoesNotExist

            # Create Thread
            thread = self.create(
                user_creator=user,
                post=post,
                content=content,
            )

            # Incr total comment post
            ForumPost.objects.incr_comment(post.id)

            # Check if have parent_thread_id
            if parent_thread_id:
                parent_thread = self.filter(id=parent_thread_id).first()

                if not parent_thread:
                    raise ObjectDoesNotExist

                thread.parent_thread = parent_thread
                thread.save()

                # Incr total comment parent thread
                self.incr_comment(parent_thread.id)

        return thread

    def action_like(self, fields, post_id):
        user = fields.get("user")

        from .models import ForumPostLike

        with transaction.atomic():
            post = self.filter(id=post_id).first()

            if not post:
                raise ObjectDoesNotExist

            post_like = ForumPostLike.objects.filter(user, post).first()

            if not post_like:
                post_like = self.create(user, post)
                self.incr_like(post.id)
            else:
                post_like.delete()
                self.decr_like(post.id)

        return

    def incr_like(self, thread_id):
        return self.filter(id=thread_id).update(total_like=F("total_like") + 1)

    def decr_like(self, thread_id):
        return self.filter(id=thread_id).update(total_like=F("total_like") - 1)

    def incr_comment(self, thread_id):
        return self.filter(id=thread_id).update(total_comment=F("total_comment") + 1)

    def decr_comment(self, thread_id):
        return self.filter(id=thread_id).update(total_comment=F("total_comment") - 1)
