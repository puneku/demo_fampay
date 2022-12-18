import asyncio
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from fampay.settings import YT_API_KEY
from . import serializers
from celery import shared_task


async def make_api_call(query_keyword=None):
    # Make the API call
    API_ENDPOINT = "https://www.googleapis.com/youtube/v3"

    # Build the API service
    service = build("youtube", "v3", developerKey=YT_API_KEY)

    # Set the search query
    query = query_keyword

    # Search for videos matching the query
    response = service.search().list(
        part="id,snippet",
        type="video",
        forDeveloper=True,
        order="date",
        publishedAfter=datetime.strftime(datetime.utcnow()-timedelta(seconds=10), "%Y-%m-%dT%H:%M:%SZ"),
        q=query,
        maxResults=10,
    ).execute()

    payload = []
    for item in response.get("items", []):
        payload.append({
            "video_title": item.get("snippet", {}).get("title", ""),
            "video_description": item.get("snippet", {}).get("description", ""),
            "published_date": item.get("snippet", {}).get("publishedAt", ""),
            "thumbnail_url": item.get("snippet", {}).get("thumbnails", {}).get("medium", {}).get("url", ""),
            "video_url": "https://www.youtube.com/watch?v={}".format(item.get("id", {}).get("videoId"))
        })

    if payload and isinstance(payload, list):
        for dt in payload:
            # update every video. Data Duplicacy not handled.
            try:
                serializer = serializers.YoutubeVideosSerializer(data=dt)
                if serializer.is_valid():
                    serializer.save()
            except:
                print("Something went wrong with YoutubeVideosSerializer.")


async def main(query_keyword=None):
    # Run the API call every 10 seconds
    while True:
        await make_api_call(query_keyword)
        await asyncio.sleep(30)


@shared_task
def auto_add_videos(query_keyword="football"):
    asyncio.run(main(query_keyword=query_keyword))
    print("Hello from the background task!")
