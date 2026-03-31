from rest_framework import generics, viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, ScoreLog
from .serializers import (UserRegisterSerializer, CustomTokenObtainPairSerializer, UserMeSerializer, RankingSerializer, UserSearchSerializer, ScoreLogSerializer)
from .permission import IsOwner

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserMeView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = UserMeSerializer

    def get_object(self):
        return self.request.user

class RankingView(generics.ListAPIView):
    queryset = User.objects.all().order_by("-score")
    serializer_class = RankingSerializer
    pagination_class = None

class UserSearchView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSearchSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["nickname", "student_id"]

class ScoreLogView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ScoreLogSerializer
    def get_queryset(self):
        return ScoreLog.objects.filter(user=self.request.user).order_by("-created_at")