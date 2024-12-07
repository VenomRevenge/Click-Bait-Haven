from django.contrib import admin
from unfold.admin import ModelAdmin
from articles.models import Article, Comment, Tag


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']
    list_filter = ['name']


@admin.register(Article)
class ArticleAdmin(ModelAdmin):

    list_display = [
        'title',
        'author',
        'is_approved',
        'created_at',
    ]

    search_fields = [
        'title',
        'author__user__username'
    ]

    list_filter = [
        'is_approved',
        'author',
        'tags',
    ]

    ordering = ['-created_at']


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = [
        'author', 
        'article', 
        'content', 
        'created_at',
    ]

    list_filter = [
        'created_at', 
        'author',
    ]

    search_fields = [
        'author__user__username', 
        'content',
    ]

    ordering = ['-created_at']