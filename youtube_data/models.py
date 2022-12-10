from django.db import models

class YoutubeVideos(models.Model):
    video_title = models.CharField(max_length=100)
    video_description = models.TextField()
    published_date = models.DateTimeField() 
    thumbnail_url = models.URLField()
    video_url = models.URLField()
