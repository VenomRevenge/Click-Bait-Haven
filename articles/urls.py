from django.urls import path, include
from articles.views import ArticleCreate


urlpatterns = [
    path('create/', ArticleCreate.as_view(), name="article_create"),
]