from rest_framework import serializers
from .models import Post ,Like, Comment

class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "user", "username", "image", "caption", "created_at", "likes_count", "comments_count"]
        read_only_fields = ["user", "likes_count", "comments_count"]

class LikeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Like
        fields = ["id", "user", "username", "post", "created_at"]
        read_only_fields = ["user"]
    
class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "username", "post", "text", "created_at"]
        read_only_fields = ["user"]