from django.urls import path, include
from fetch_api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('find_videos', views.VideosAPIView, basename='find-videos')
#router.register('search', views.search_videos.as_view())
urlpatterns = [
    path("", include(router.urls)),
]