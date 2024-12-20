from django.urls import path, include
from moderation_system.views import approve_article, article_review, deleted_articles, reject_article


urlpatterns = [
    path('review/', article_review, name='review_page'),
    path('deleted/', deleted_articles, name='deleted_articles'),
    path('approve-article/<int:pk>/', approve_article, name='approve_article'),
    path('reject-article/<int:pk>/', reject_article, name='reject_article'),
]