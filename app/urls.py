from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('watch/<int:video_id>/', views.watch_video, name='watch_video'),
    path('play_simple/<int:video_id>/', views.play_video_simple, name='play_video_simple'),
    path('tv-series/', views.tv_series_list, name='tv_series_list'),
    path('movies/', views.movies, name='movies'),
    path('login/', views.loginUser, name='login'),
    path('signup/', views.signupUser, name='signup'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/<int:pk>/', views.profile, name='profile'),   
]
