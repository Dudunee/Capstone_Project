from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model. Handles creating a user with a hashed password.
    """

    class Meta:
        model = User
        fields = ["id", "email", "username", "password"]

    def create(self, validated_data):
        """
        Overriding the default create method to hash the password before saving the user.
        """
        user = User(
            email=validated_data["email"], username=validated_data.get("username", "")
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
