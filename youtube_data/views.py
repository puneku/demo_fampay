from django.shortcuts import render
from django.http import HttpResponse
from youtube_data.serializers import YoutubeVideosSerializer
from .models import YoutubeVideos
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from django.db.models import Q
from .tasks import auto_add_videos

def home(request):
    '''V1 approach to call Youtube APIs using asyncio'''
    # auto_add_videos.delay()
    return HttpResponse("<div style='text-align:center'><h1>Hello, Fampay!</h1></div>")


class Videos(APIView):

    def get(self, request):
        pattern = request.GET.get('pattern')
        page = request.GET.get('page', 1)
        per_page_count = request.GET.get('per_page_count', 5)
        videos_list = YoutubeVideos.objects.filter(Q(video_title__contains=pattern) | Q(video_description__contains=pattern)).order_by('-published_date')
        paginator = Paginator(videos_list, per_page_count)
        curr_page_data = paginator.get_page(page) 
        serializer = YoutubeVideosSerializer(curr_page_data, many=True)
        # Case: when we want to store videos corresponding to user's search query (V1 approch)
        # auto_add_videos.delay()
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        if data and isinstance(data, list):
            for dt in data:
                serializer = YoutubeVideosSerializer(data=dt)
                if serializer.is_valid():
                    serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        serializer = YoutubeVideosSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)