from . import models
import time
from googleapiclient.discovery import build
from background_task import background
from django.db import connections
from collections import deque


## Using Stack to optimise the time for taking a key
API_KEYS = open('fetch_api/example_keys.txt').read().split('\n')
API_KEYS_STACK = deque()

YOUTUBE_API_SERVICE = "youtube"
YOUTUBE_API_VERSION = "v3"

# Invterval after which the background process again continues
INTERVAL_TIME_FOR_PROCESS = 10

for key in API_KEYS:
    API_KEYS_STACK.append(key)

# Dictionary to store the video ids for the videos so that no duplicate exist in api response
def video_ids_set():
    ids_set = {}
    for data in models.Video.objects.all().iterator():
        ids_set[data] = 1
    return ids_set
    


def get_response_with_automated_key_optimisation():
    # Checking a call can be made through any key or not and then deleting the key which is exhausted
    while not API_KEYS_STACK.empty():
        key = API_KEYS_STACK.pop()
        try:
            youtube_object = build(YOUTUBE_API_SERVICE, YOUTUBE_API_VERSION, developerKey=key)
            response = youtube_object.search().list(q="cricket", part="id, snippet", maxResults=100).execute()
            if str(response) != '<Response [403]>':
                API_KEYS_STACK.append(key)
                return (response, key)
        except:
            continue
    return (None, None)


# Background process for fetching the videos from youtube and storing in our database
@background()
def schelude_jobs():
    video_set = video_ids_set()
    while True:
        time.sleep(INTERVAL_TIME_FOR_PROCESS)
        json_response, current_key = None, None
        json_response, current_key = get_response_with_automated_key_optimisation()
        if json_response == None:
            print("Quota for all keys is finished or internal Error")
            return 
        if current_key == None:
            print("Quota for all keys is finished")
            return
        for fetched_video in json_response["items"]:
            try:
                # Storing the video model after fetching throungh youtube
                vid_id = fetched_video['id']['videoId']
                if (video_set.get(vid_id) == None):
                    Id = fetched_video['id']['videoId']
                    Snippet = fetched_video['snippet']
                    Title = Snippet['title']
                    Published_at = Snippet['publishedAt']
                    Description = Snippet['description']
                    Thumbnail = Snippet['thumbnails']['default']
                    Thumbnail_url = Thumbnail['url']
                    video_model = models.Video(vid_id=Id, title=Title, description=Description, published_at=Published_at, thumbnail_url=Thumbnail_url)
                    video_model.save()
                    # Storing the meta data associated with video in separte table
                    meta_datas = [{'thumbnail_size': thumbnail_size, 'thumbnail_url': Snippet['thumbnails'][thumbnail_size]['url'],} for thumbnail_size in Snippet['thumbnails']]
                    for meta_data in meta_datas:
                        meta_data['current_video'] = video_model
                        meta_obj = models.VideoMetaData(**meta_data)
                        meta_obj.save()
            except:
                continue
        for conn in connections.all():
            conn.close()
            