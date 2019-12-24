
from django.urls import path, include
from .views import (
    ProfileLoad, LoginAPIView, RegisterAPIView, UpdateProfile, ProfilePictureUpdate, Test
)


urlpatterns = [
    path('profile/auth/', LoginAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('<username>/', ProfileLoad.as_view()),
    path('<username>/update/', UpdateProfile.as_view()),
    path('<username>/update2/', Test.as_view()),
    path('<username>/pic-update/', ProfilePictureUpdate.as_view()),
]