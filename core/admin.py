from django.contrib import admin
from .models import Skill, UserProfile, Post, Message, Event

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'open_to_work')
    list_filter = ('open_to_work',)
    search_fields = ('user__username', 'bio')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_type', 'created_at')
    list_filter = ('post_type', 'created_at')
    search_fields = ('user__username', 'content')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'status', 'processing_time', 'timestamp')
    list_filter = ('event_type', 'status', 'timestamp')
    search_fields = ('event_type',)
    readonly_fields = ('timestamp', 'processing_time')
