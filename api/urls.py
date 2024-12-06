from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from api.views import ListArticles, RetrieveSingleArticle, ViewTags


urlpatterns = [
    # swagger views
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # my api views
    path('articles/', ListArticles.as_view(), name='articles_api'),
    path('article/<int:id>/', RetrieveSingleArticle.as_view(), name='article_api'),
    path('tags/', ViewTags.as_view(), name='tags_all_api'),
]