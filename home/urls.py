from django.urls import path, include
from home.views import Register, SignIn, about, contact_us, delete_notification, index, my_notifications, privacy_policy, random_article, sign_out


urlpatterns = [
    path('', index, name='index'),
    path('register/', Register.as_view(), name='register'),
    path('sign-in/', SignIn.as_view(), name='sign_in'),
    path('sign-out/', sign_out, name='sign_out'),
    path('random/', random_article, name='random_article'),
    path('contact-us/', contact_us, name='contact_us'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('about/', about, name='about'),
    path('my-notifications/',include([
        path('', my_notifications, name='my_notifications'),
        path('<int:pk>/delete/', delete_notification, name='delete_notification'),
        ]) 
    ),
]