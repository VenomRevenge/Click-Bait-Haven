from django.urls import path

from home.views import Register, SignIn, index, sign_out


urlpatterns = [
    path('', index, name='index'),
    path('register/', Register.as_view(), name='register'),
    path('sign-in/', SignIn.as_view(), name='sign_in'),
    path('sign-out/', sign_out, name='sign_out')
]