import logging
import pickle
from django.db.models import Exists
from rest_framework import serializers
from app.utils.redis import redis_client as cache
from .models import ForumPost, ForumPostPicture, ForumThread, ForumThreadLike, Status

logger = logging.getLogger(__name__)

THREAD_KEY = "forum_thread_{}_{}"
SUB_THREAD_KEY = "forum_sub_thread_{}_{}"


class PassSerializer:
    def __init__(self, data, *args, **kwargs):
        self.data = data

    def is_valid(self):
        return True


def get_user(context):
    request = context.get("request")
    if request and hasattr(request, "user"):
        return request.user
    else:
        return context["user"]


class ForumPostListQueryParamsSerializer(serializers.Serializer):
    page = serializers.IntegerField(default=0)
    limit = serializers.IntegerField(default=10)
    order_by = serializers.CharField(default="-created_at")
    category = serializers.IntegerField()
    latitude = serializers.FloatField()
    longtitude = serializers.FloatField()

    def validate_order_by(self, data):
        if data != 1 or data != 2:
            raise serializers.ValidationError("category only allowed with id 1 or 2")
        return data


class CreateForumPostSerializer(serializers.Serializer):
    latitude = serializers.FloatField(required=True)
    longtitude = serializers.FloatField(required=True)
    title = serializers.CharField(required=True)
    content = serializers.CharField(required=True)
    category = serializers.IntegerField(required=True)

    def validate_order_by(self, data):
        if data != 1 or data != 2:
            raise serializers.ValidationError("category only allowed with id 1 or 2")
        return data


class CreateForumThreadSerializer(serializers.Serializer):
    parent_thread_id = serializers.IntegerField(required=False, default=None)
    content = serializers.CharField(required=True)


class ThreadSerializer(serializers.ModelSerializer):
    user_creator = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    content = serializers.CharField()
    total_like = serializers.IntegerField()
    total_comment = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    sub_threads = serializers.SerializerMethodField()

    def get_user_creator(self, obj):
        return obj.user_creator

    def get_is_like(self, obj):
        try:
            return obj.thread_like_exist
        except Exception as e:
            logger.error("error when thread serializer at get_is_like => {}".format(e))
            return False

    def get_sub_threads(self, obj):
        user = get_user(self.context)
        user_id = None if user.is_anonymous else user.id

        sub_thread = cache.get(SUB_THREAD_KEY.format(obj.id, user_id))
        if not sub_thread:
            sub_thread = obj.sub_thread.filter(status=Status.ACTIVE).select_related(
                "user_creator"
            )
            if not user.is_anonymous:
                sub_thread.annotate(
                    thread_like_exists=Exists(
                        ForumThreadLike.objects.filter(
                            user=user,
                        ),
                    ),
                )
            cache.set(
                SUB_THREAD_KEY.format(obj.id, user_id),
                pickle.dumps(sub_thread),
                3600,  # 1 hour
            )
        else:
            sub_thread = pickle.loads(sub_thread)

        return ThreadSerializer(
            instance=sub_thread,
            many=True,
            context={"user": user},
        ).data

    class Meta:
        model = ForumThread
        fields = (
            "user_creator",
            "sub_threads",
            "is_like",
            "content",
            "total_like",
            "total_comment",
            "created_at",
            "updated_at",
        )


class ForumPostPictureSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()

    def get_picture(self, obj):
        return obj.get_picture()

    class Meta:
        model = ForumPostPicture
        fields = ("picture",)


class ForumListSerializer(serializers.ModelSerializer):
    user_creator = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    title = serializers.CharField()
    category = serializers.CharField()
    total_like = serializers.IntegerField()
    total_comment = serializers.IntegerField()
    total_view = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def get_user_creator(self, obj):
        return obj.user_creator

    def get_location(self, obj):
        return obj.location

    def get_is_like(self, obj):
        try:
            return obj.post_like_exist
        except Exception as e:
            logger.error("error when post serializer at get_is_like => {}".format(e))
            return False

    class Meta:
        model = ForumPost
        fields = "__all__"


class ForumDetailSerializer(serializers.ModelSerializer):
    user_creator = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    title = serializers.CharField()
    content = serializers.CharField()
    category = serializers.CharField()
    total_like = serializers.IntegerField()
    total_comment = serializers.IntegerField()
    total_view = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    pictures = serializers.SerializerMethodField
    threads = serializers.SerializerMethodField()

    def get_user_creator(self, obj):
        return obj.user_creator

    def get_location(self, obj):
        return obj.location

    def get_is_like(self, obj):
        try:
            return obj.post_like_exist
        except Exception as e:
            logger.error("error when post serializer at get_is_like => {}".format(e))
            return False

    def get_pictures(self, obj):
        return ForumPostPictureSerializer(
            instance=obj.forum_post_picture,
            Many=True,
        ).data

    def get_threads(self, obj):
        user = get_user(self.context)
        user_id = None if user.is_anonymous else user.id

        thread = cache.get(THREAD_KEY.format(obj.id, user_id))
        if not thread:
            thread = obj.thread.filter(
                parent_thread=None,
                status=Status.ACTIVE,
            ).select_related("user_creator")
            if not user.is_anonymous:
                thread.annotate(
                    thread_like_exists=Exists(
                        ForumThreadLike.objects.filter(
                            user=user,
                        ),
                    ),
                )
            cache.set(
                THREAD_KEY.format(obj.id, user_id),
                pickle.dumps(thread),
                3600,  # 1 hour
            )
        else:
            thread = pickle.loads(thread)

        return ThreadSerializer(
            instance=thread,
            many=True,
            context={"user": user},
        )

    class Meta:
        model = ForumPost
        fields = (
            "user_creator",
            "location",
            "is_like",
            "title",
            "content",
            "category",
            "total_like",
            "total_comment",
            "total_view",
            "created_at",
            "updated_at",
            "pictures",
            "threads",
        )
