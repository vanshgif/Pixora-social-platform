from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from .models import Follow
from .serializers import UserSerializer, FollowSerializer

User = get_user_model()

# ✅ List all users (GET) and create a user (POST) 
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# ✅ Signup (register new user)
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# ✅ Profile (view/update own profile)
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Return logged-in user's profile"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        """Update logged-in user's profile"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

# ✅ Follow / Unfollow
class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        """Follow another user"""
        try:
            target_user = User.objects.get(id=user_id)
            if target_user == request.user:
                return Response({"error": "You cannot follow yourself"}, status=400)

            follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)
            if created:
                return Response({"message": f"You are now following {target_user.username}"})
            return Response({"message": "You already follow this user"})

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

    def delete(self, request, user_id):
        """Unfollow a user"""
        try:
            follow = Follow.objects.get(follower=request.user, following_id=user_id)
            follow.delete()
            return Response({"message": "Unfollowed successfully"})
        except Follow.DoesNotExist:
            return Response({"error": "You are not following this user"}, status=400)

# ✅ Followers list for any user
class FollowersListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        """Get all followers of a user"""
        try:
            user = User.objects.get(id=user_id)
            followers = user.followers.all().select_related("follower")
            data = [UserSerializer(f.follower).data for f in followers]
            return Response(data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

# ✅ Following list for any user
class FollowingListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        """Get all users a user is following"""
        try:
            user = User.objects.get(id=user_id)
            following = user.following.all().select_related("following")
            data = [UserSerializer(f.following).data for f in following]
            return Response(data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
