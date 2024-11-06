from django.urls import path

from home.views import Register, SignIn, index


urlpatterns = [
    path('', index, name='index'),
    path('register/', Register.as_view(), name='register'),
    path('sign-in/', SignIn.as_view(), name='sign_in')
]