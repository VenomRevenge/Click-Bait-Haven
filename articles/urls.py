from django.urls import path, include
from articles.views import ArticleCreate, article_search, article_view, delete_comment, edit_comment, post_comment, react_to_article, react_to_comment


urlpatterns = [
    path('search/', article_search, name='article_search'),
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/', include([
        path('', article_view, name='article'),
        path('react/', react_to_article, name='article_react'),
        path('comment/', include([
            path('post-comment/', post_comment, name='post_comment'),
            path('<int:comment_pk>/edit-comment/', edit_comment, name='edit_comment'),
            path('<int:comment_pk>/delete-comment/', delete_comment, name='delete_comment'),
            path('<int:comment_pk>/react/', react_to_comment, name='comment_react'),
        ]))
    ]))
]