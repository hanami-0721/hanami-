from django.urls import path
from . import views

urlpatterns = [
    path('', views.MissionListAPIView.as_view(), name='mission-list'),
    path('create/', views.MissionCreateAPIView.as_view(), name='mission-create'),

    path('drafts/', views.DraftListAPIView.as_view(), name='draft-list'),
    path('drafts/create/', views.DraftCreateAPIView.as_view(), name='draft-create'),
    path('drafts/<int:pk>/update/', views.DraftUpdateAPIView.as_view(), name='draft-update'),
    path('drafts/<int:pk>/delete/', views.DraftDeleteAPIView.as_view(), name='draft-delete'),

    path('<int:pk>/accept/', views.MissionAcceptAPIView.as_view(), name='mission-accept'),
    path('<int:pk>/complete/', views.MissionCompleteAPIView.as_view(), name='mission-complete'),
    path('<int:pk>/cancel/', views.MissionCancelAPIView.as_view(), name='mission-cancel'),

    path('my/published/', views.MyPublishedMissionsAPIView.as_view(), name='my-published'),
    path('my/accepted/', views.MyAcceptedMissionsAPIView.as_view(), name='my-accepted'),

    path('admin/<int:pk>/update/', views.AdminMissionUpdateAPIView.as_view(), name='admin-mission-update'),
]