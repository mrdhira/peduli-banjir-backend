from rest_framework import permissions
from rest_framework.views import APIView
from app.utils.http import generic_get, generic_post, generic_put
from .models import ForumPost, ForumThread
from .serializers import (
    PassSerializer,
    ForumPostListQueryParamsSerializer,
    ForumListSerializer,
    ForumDetailSerializer,
    ThreadSerializer,
    CreateForumPostSerializer,
    CreateForumThreadSerializer,
    ForumPostLikeSerializer,
    ForumThreadLikeSerializer,
)


class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user and request.user.is_authenticated


# Create your views here.
class ForumPostView(APIView):
    permission_classes = (CustomPermission,)

    # GET Forum Post List
    def get(self, request):
        return generic_get(
            request=request,
            model_method=ForumPost.objects.get_post,
            request_serializer=ForumPostListQueryParamsSerializer,
            response_serializer=ForumListSerializer,
            many=True,
            protected=True,
        )

    # POST Create Forum Post
    def post(self, request):
        return generic_post(
            request=request,
            create_method=ForumPost.objects.create_post,
            request_serializer=CreateForumPostSerializer,
            response_serializer=ForumDetailSerializer,
            protected=True,
        )


class ForumPostDetailView(APIView):
    permission_classes = (CustomPermission,)

    # GET Forum Post Detail
    def get(self, request, post_id):
        return generic_get(
            request=request,
            model_method=ForumPost.objects.get_post_detail,
            request_serializer=PassSerializer,
            response_serializer=ForumDetailSerializer,
            context={
                "post_id": post_id,
            },
            protected=True,
        )


class ForumPostLikeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # PUT Like / Unlike Forum Post
    def put(self, request, post_id):
        return generic_put(
            request=request,
            update_method=ForumPost.objects.action_like,
            request_serializer=PassSerializer,
            response_serializer=ForumPostLikeSerializer,
            object_id=post_id,
            context={
                "post_id": post_id,
            },
            protected=True,
        )


class ForumPostThreadView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # POST Create Forum Thread / Comment
    def post(self, request, post_id):
        return generic_post(
            request=request,
            create_method=ForumThread.objects.create_thread,
            request_serializer=CreateForumThreadSerializer,
            response_serializer=ThreadSerializer,
            context={
                "post_id": post_id,
            },
            protected=True,
        )


class ForumThreadLikeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # PUT Like / Unlike Forum Thread
    def put(self, request, post_id, thread_id):
        return generic_put(
            request=request,
            update_method=ForumThread.objects.action_like,
            request_serializer=PassSerializer,
            response_serializer=ForumThreadLikeSerializer,
            object_id=thread_id,
            context={
                "post_id": post_id,
                "thread_id": thread_id,
            },
            protected=True,
        )
