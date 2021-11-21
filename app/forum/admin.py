import nested_admin
from django.contrib import admin

# Register your models here.
from .models import ForumPost, ForumPostLike, ForumThread, ForumThreadLike


class ThreadLikeInline(nested_admin.NestedStackedInline):
    model = ForumThreadLike
    extra = 0
    fields = [
        "user",
    ]


class ThreadInline(nested_admin.NestedStackedInline):
    model = ForumThread
    extra = 0
    fields = [
        "parent_thread",
        "content",
        "total_like",
        "total_comment",
        "status",
    ]
    inlines = [ThreadLikeInline]


class PostLikeInline(nested_admin.NestedStackedInline):
    model = ForumPostLike
    extra = 0
    fields = [
        "user",
    ]


class PostAdmin(nested_admin.NestedModelAdmin):
    list_display = (
        "creator_name",
        "location_address",
        "title",
        "category",
        "status",
        "total_like",
        "total_comment",
        "total_view",
    )

    search_fields = (
        "user_creator__full_name",
        "location__address",
        "title",
    )

    list_filter = ("status",)

    def creator_name(self, obj):
        return obj.user_creator.full_name

    creator_name.short_description = "User Creator Name"
    creator_name.admin_order_field = "user_creator__full_name"

    def location_address(self, obj):
        return obj.location.address

    location_address.short_description = "Location Address"
    location_address.admin_order_field = "location__address"

    inlines = [
        PostLikeInline,
        ThreadInline,
    ]


class ThreadAdmin(nested_admin.NestedModelAdmin):
    list_display = (
        "creator_name",
        "post_title",
        "content",
        "status",
        "total_like",
        "total_comment",
    )

    search_fields = (
        "user_creator__full_name",
        "post__title",
    )

    list_filter = ("status",)

    def creator_name(self, obj):
        return obj.user_creator.full_name

    creator_name.short_description = "User Creator Name"
    creator_name.admin_order_field = "user_creator__full_name"

    def post_title(self, obj):
        return obj.post.title

    creator_name.short_description = "Post Title"
    creator_name.admin_order_field = "post__tilte"


admin.site.register(ForumPost, PostAdmin)
admin.site.register(ForumThread, ThreadAdmin)
