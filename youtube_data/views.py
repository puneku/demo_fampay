from django.shortcuts import render
from django.http import HttpResponse
from youtube_data.serializers import YoutubeVideosSerializer
from .models import YoutubeVideos
from rest_framework.views import APIView
from rest_framework.response import Response

def home(request):    
    return HttpResponse("<div style='text-align:center'><h1>Hello, Fampay!</h1></div>")

# def videos(request):
#     if request.method == "GET":
#         pass

class Videos(APIView):

    def get(self, request):
        videos_list = YoutubeVideos.objects.all()
        serializer = YoutubeVideosSerializer(videos_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = YoutubeVideosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)