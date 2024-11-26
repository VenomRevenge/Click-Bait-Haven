from django.urls import path, include
from articles.views import ArticleCreate, article_search, article_view


urlpatterns = [
    path('search/', article_search, name='article_search'),
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/', include([
        path('', article_view, name='article'),
    ]))
]