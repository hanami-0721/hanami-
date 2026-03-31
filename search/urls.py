from django.urls import path
from . import views

urlpatterns = [
    path('missions/', views.SearchMissionView.as_view(), name='search-missions'),
    path('users/', views.SearchUserView.as_view(), name='search-users'),
]