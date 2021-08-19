# Checking and testing the api
from googleapiclient.discovery import build

youtube_object = build("youtube", "v3", developerKey="AIzaSyADhBWcSeJGGER9zyqndzQTjiX9x1ZXeu0")
response = youtube_object.search().list(q="cricket", part="id, snippet", maxResults=100).execute()
print(response)