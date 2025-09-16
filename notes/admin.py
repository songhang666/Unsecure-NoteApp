from django.contrib import admin
from .models import Note, Comment

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_public', 'comment_count')
    list_filter = ('is_public', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'author_username', 'author_userprofile_full_name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = 'Comments'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'note', 'created_at', 'content_preview')
    list_filter = ('created_at',)
    search_fields = ('content', 'author_username', 'note_title')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'