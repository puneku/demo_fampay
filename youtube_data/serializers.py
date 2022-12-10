from rest_framework import serializers
from .models import YoutubeVideos

class YoutubeVideosSerializer(serializers.ModelSerializer):
    '''Conversion from SQL data to JSON format'''
    class Meta:
        '''Similer to projection (in MONGODB)'''
        model = YoutubeVideos
        # fields = ('video_title', 'video_description', 'video_url')
        fields = '__all__'
