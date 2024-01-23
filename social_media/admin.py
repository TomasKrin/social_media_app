from django.contrib import admin

from social_media.models import Profile, UserPost, PostComment


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'profile_views', 'profile_pic')
    list_filter = ('user', 'display_name',)
    list_editable = ('display_name', 'profile_pic',)
    search_fields = ('user', 'display_name',)
    fieldsets = (
        ('Profile', {'fields': ('display_name', 'profile_pic')}),
    )


class UserPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_posted', 'profile', 'post',)
    list_filter = ('date_posted', 'profile',)
    search_fields = ('profile__display_name', 'profile__user__username')
    fieldsets = (
        ('Post', {'fields': ('post', 'img')}),
    )


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('date_posted', 'get_post_id', 'profile', 'comment',)
    list_filter = ('date_posted', 'profile',)
    search_fields = ('profile__display_name', 'profile__user__username')
    fieldsets = (
        ('Comment', {'fields': ('comment',)}),
    )


admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserPost, UserPostAdmin)
admin.site.register(PostComment, PostCommentAdmin)
