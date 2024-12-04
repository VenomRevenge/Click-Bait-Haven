from django.urls import path, include
from home.views import Register, SignIn, delete_notification, index, my_notifications, random_article, sign_out


urlpatterns = [
    path('', index, name='index'),
    path('register/', Register.as_view(), name='register'),
    path('sign-in/', SignIn.as_view(), name='sign_in'),
    path('sign-out/', sign_out, name='sign_out'),
    path('random/', random_article, name='random_article'),
    path('my-notifications/',include([
        path('', my_notifications, name='my_notifications'),
        path('<int:pk>/delete/', delete_notification, name='delete_notification'),
        ]) 
    ),
]