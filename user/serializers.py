from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework import serializers


def validate_password(value):
    if len(value) < 6:
        raise serializers.ValidationError("Password must be at least 6 characters")
    if not any(char.isdigit() for char in value):
        raise serializers.ValidationError("Password must contain at least one digit")
    if not any(char.isupper() for char in value):
        raise serializers.ValidationError("Must be at least one uppercase letter")
    return value


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        validators=[MinLengthValidator(2), MaxLengthValidator(20)]
    )
    last_name = serializers.CharField(
        validators=[MinLengthValidator(2), MaxLengthValidator(30)]
    )
    password = serializers.CharField(
        write_only=True,
        help_text=(
            "Password must be at least 6 characters long, "
            "contain only latin letters "
            "(at least one Uppercase letter) and numbers."
        ),
        style={"input_type": "password"},
        validators=[
            validate_password,
        ],
    )

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "first_name", "last_name", "password", "is_staff")
        read_only_fields = ("is_staff",)
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 6,
                "style": {"input_type": "password"},
                "label": "Password",
            }
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=6,
        style={"input_type": "password"},
        validators=[
            validate_password,
        ],
    )
    balance = serializers.IntegerField(min_value=0)
    profile_pic = serializers.ImageField(required=False)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "profile_pic",
            "balance",
            "password",
        )

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user
