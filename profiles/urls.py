from django.urls import path, include
from profiles.views import ProfileDetails, ProfileEdit


urlpatterns = [
    path('<int:pk>/', include([
        path('details/', ProfileDetails.as_view(), name='profile_details'),
        path('edit/', ProfileEdit.as_view(), name='profile_edit'),
    ]))
]
