from django.urls import path
from .views import (
    UserListCreateView, UserRegisterView, ProfileView, FollowUserView,
    FollowersListView, FollowingListView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # 👤 Auth & User
    path("users/", UserListCreateView.as_view(), name="user-list-create"),  # List + create users
    path("register/", UserRegisterView.as_view(), name="user-register"),    # Register
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # Login (JWT)
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"), # Refresh JWT
    path("profile/", ProfileView.as_view(), name="user-profile"),            # Profile (view/update)

    # 👥 Follow System
    path("follow/<int:user_id>/", FollowUserView.as_view(), name="follow-user"),  # Follow/unfollow
    path("followers/", FollowersListView.as_view(), name="followers-list"),      # Get my followers
    path("following/", FollowingListView.as_view(), name="following-list"),      # Get my following
]
