from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('feed/', views.feed, name='feed'),
    path('explore/', views.explore, name='explore'),
    path('<slug:username>/status/<int:id>/', views.SingleStatusView.as_view(), name='single_status'),
    path('<slug:username1>/following/user/<slug:username2>/', views.follow, name='follow'),
    path('<slug:username>/likes/status/<int:id>/', views.likes, name='likes'),
    path('<slug:username>/status/new/', views.NewStatusView.as_view(), name='new_status'),
    path('<slug:username>/settings/', views.SettingsView.as_view(), name='settings'),
    path('<slug:username>/', views.profile, name='profile'),
]