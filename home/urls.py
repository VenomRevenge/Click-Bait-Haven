from django.urls import path

from home.views import Register, index


urlpatterns = [
    path('', index, name='index'),
    path('register/', Register.as_view(), name='register')
]