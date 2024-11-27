from django.urls import path, include
from moderation_system.views import article_review


urlpatterns = [
    path('review/', article_review, name='review_page'),
]