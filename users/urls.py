from django.urls import path
from .views import UserListCreateView, UserRegisterView, ProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("users/", UserListCreateView.as_view(), name="user-list-create"),
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileView.as_view(), name="user-profile"),
]
