from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Mission, MissionImage
from .serializers import *
from .permissions import *
from accounts.models import ScoreLog

class MissionListAPIView(generics.ListAPIView):
    queryset = Mission.objects.filter(is_draft=False)
    serializer_class = MissionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title', 'content']
    ordering_fields = ['reward_score', 'created_at']

class MissionCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MissionPublishSerializer

    def perform_create(self, serializer):
        mission = serializer.save(
            publisher=self.request.user,
            status='pending',
            is_draft=False
        )
        images = self.request.FILES.getlist('images', [])
        for img in images[:3]:
            MissionImage.objects.create(mission=mission, image=img)

class DraftCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MissionDraftSerializer

    def perform_create(self, serializer):
        serializer.save(publisher=self.request.user)

class DraftUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsPublisher]
    serializer_class = MissionDraftSerializer
    queryset = Mission.objects.filter(is_draft=True)

class DraftDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsPublisher]
    queryset = Mission.objects.filter(is_draft=True)

class DraftListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MissionSerializer

    def get_queryset(self):
        return Mission.objects.filter(publisher=self.request.user, is_draft=True)

class MissionAcceptAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Mission.objects.all()

    def post(self, request, pk):
        mission = self.get_object()
        mission.acceptor = request.user
        mission.status = 'in_progress'
        mission.save()
        return Response({"msg": "接取成功"})

class MissionCompleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsPublisher]
    queryset = Mission.objects.all()

    def post(self, request, pk):
        mission = self.get_object()
        mission.status = 'completed'
        mission.save()
        if mission.acceptor:
            mission.acceptor.score += mission.reward_score
            mission.acceptor.save()
            ScoreLog.objects.create(
                user=mission.acceptor,
                score_change=mission.reward_score,
                source='mission_complete'
            )
        return Response({"msg": "委托已完成，积分已发放"})

class MissionCancelAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsPublisher]
    queryset = Mission.objects.all()

    def post(self, request, pk):
        mission = self.get_object()
        mission.status = 'cancelled'
        mission.save()
        return Response({"msg": "委托已撤销"})

class MyPublishedMissionsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MissionSerializer

    def get_queryset(self):
        return Mission.objects.filter(publisher=self.request.user, is_draft=False)

class MyAcceptedMissionsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MissionSerializer

    def get_queryset(self):
        return Mission.objects.filter(acceptor=self.request.user, status__in=['in_progress','completed'])

class AdminMissionUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsPartAdmin]
    serializer_class = MissionSerializer
    queryset = Mission.objects.all()