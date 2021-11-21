from django.urls import path
from .views import (
    ForumPostView,
    ForumPostDetailView,
    ForumPostLikeView,
    ForumPostThreadView,
    ForumThreadLikeView,
)

app_name = "forum"
urlpatterns = [
    path(
        "",
        view=ForumPostView.as_view(),
        name="forum_post",
    ),
    path(
        "<post_id>",
        view=ForumPostDetailView.as_view(),
        name="forum_post_detail",
    ),
    path(
        "<post_id>/like",
        view=ForumPostLikeView.as_view(),
        name="forum_post_like",
    ),
    path(
        "<post_id>/comment",
        view=ForumPostThreadView.as_view(),
        name="forum_post_thread",
    ),
    path(
        "<post_id>/<thread_id>/like",
        view=ForumThreadLikeView.as_view(),
        name="forum_thread_like",
    ),
]
