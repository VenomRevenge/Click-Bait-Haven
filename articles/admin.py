from django.contrib import admin

from articles.models import Article, Tag

# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    ...


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    ...