from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, ScoreLog
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["student_id", "nickname", "email", "password", "password_confirm"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("两次密码不一致")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["nickname"] = user.nickname
        token["student_id"] = user.student_id
        token["is_part_admin"] = user.is_part_admin
        return token


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["student_id", "nickname", "email", "score", "is_part_admin"]
        read_only_fields = ["score", "student_id", "is_part_admin"]


class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["student_id", "nickname", "score"]


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["student_id", "nickname", "score"]


class ScoreLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreLog
        fields = "__all__"