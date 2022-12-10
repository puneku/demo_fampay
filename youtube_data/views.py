from django.shortcuts import render
from django.http import HttpResponse
from youtube_data.serializers import YoutubeVideosSerializer
from .models import YoutubeVideos
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator

def home(request):    
    return HttpResponse("<div style='text-align:center'><h1>Hello, Fampay!</h1></div>")

# def videos(request):
#     if request.method == "GET":
#         pass

class Videos(APIView):

    def get(self, request):
        page = request.GET.get('page', 1)
        per_page_count = request.GET.get('per_page_count', 5)
        videos_list = YoutubeVideos.objects.all().order_by('-published_date')
        paginator = Paginator(videos_list, per_page_count)
        curr_page_data = paginator.get_page(page) 
        serializer = YoutubeVideosSerializer(curr_page_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = YoutubeVideosSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)