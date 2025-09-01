from rest_framework import generics, permissions, status

from users import models
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# ✅ Create & List all posts
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ✅ Retrieve, Update, Delete a single post
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.request.user != self.get_object().user:
            raise PermissionError("You can only edit your own posts")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise PermissionError("You can only delete your own posts")
        instance.delete()





class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        """Like a post"""
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)

        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            post.likes_count += 1
            post.save()
            return Response({"message": "Post liked"})
        return Response({"message": "You already liked this post"})

    def delete(self, request, post_id):
        """Unlike a post"""
        try:
            like = Like.objects.get(user=request.user, post_id=post_id)
            like.delete()

            # update counter
            Post.objects.filter(id=post_id).update(
                likes_count=models.F("likes_count") - 1
            )
            return Response({"message": "Post unliked"})
        except Like.DoesNotExist:
            return Response({"error": "You haven't liked this post"}, status=400)
        




        # ✅ List & Create comments for a post
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post_id=self.kwargs["post_id"])

class PermissionDenied(Exception):
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        raise NotImplementedError

    def some_method(self, *args, **kwargs):
        raise NotImplementedError



# ✅ Update & Delete a comment
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.request.user != self.get_object().user:
            raise PermissionDenied("You can only edit your own comments")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise PermissionDenied("You can only delete your own comments")
        instance.delete()