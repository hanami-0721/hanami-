from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("me/", views.UserMeView.as_view(), name="me"),
    path("ranking/", views.RankingView.as_view(), name="ranking"),
    path("search/", views.UserSearchView.as_view(), name="user-search"),
    path("score-logs/", views.ScoreLogView.as_view(), name="score-logs"),
]