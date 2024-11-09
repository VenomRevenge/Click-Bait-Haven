from django.urls import path, include
from profiles.views import ProfileDetails, profile_edit


urlpatterns = [
    path('<int:pk>/', include([
        path('details/', ProfileDetails.as_view(), name='profile_details'),
        path('edit/', profile_edit, name='profile_edit'),
    ]))
]
