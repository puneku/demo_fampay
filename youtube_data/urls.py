import youtube_data.views as views
from django.urls import path

urlpatterns = [
    path('', views.home)
]
