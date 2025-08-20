from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # password won’t show in responses

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "bio", "profile_pic"]

    def create(self, validated_data):
        # Use Django's built-in method to hash password
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            bio=validated_data.get("bio", "")
        )
        user.set_password(validated_data["password"])  # ✅ hashes password
        user.save()
        return user
