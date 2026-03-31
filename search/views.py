from django.shortcuts import render

# Create your views here.
from rest_framework import filters
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from missions.models import Mission
from accounts.models import User
from missions.serializers import MissionSerializer
from accounts.serializers import UserSearchSerializer

class SearchMissionView(ListAPIView):
    serializer_class = MissionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # 筛选字段：状态
    filterset_fields = ['status']
    # 搜索关键词：标题、内容
    search_fields = ['title', 'content']
    # 排序：积分、时间
    ordering_fields = ['reward_score', 'created_at']

    def get_queryset(self):
        return Mission.objects.filter(is_draft=False)


class SearchUserView(ListAPIView):
    serializer_class = UserSearchSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['nickname', 'student_id']
    ordering_fields = ['score']
    ordering = ['-score']

    queryset = User.objects.all()