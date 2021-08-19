from django import forms
from django.shortcuts import render

from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, status, filters
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from . import models, forms
from django.db.models import Q
from rest_framework.response import Response
from django.http import HttpResponse
import json
from django.core import serializers


# Pagination class for paginating the Video API
class VideosPaginationAPIView(PageNumberPagination):
    page_size = 7
    max_page_size = 7


# APIView for Video API
class VideosAPIView(viewsets.ModelViewSet):
    renderer_classes = [JSONRenderer]
    serializer_class = forms.VideoSerializer
    pagination_class = VideosPaginationAPIView
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('title', 'description',)
    ordering_fields = ('title', 'vid_id', 'description')

    # Getting queryset
    def get_queryset(self):
        return models.Video.objects.all().order_by('-published_at')

    # Getting object
    def get_object(self, pk):
        if models.Video.objects.filter(pk=pk).exists():
            return models.Video.objects.get(pk=pk)
        else:
            return None
    
    # Providing Options for sorting and searching in dashboard
    def options(self, request, *args, **kwargs):
        q = request.query_params.get("q")
        query = Q(title__icontains=q)
        query |= Q(description__icontains=q)
        query_set = models.Video.objects.all().filter(query)

        serializer = forms.VideoAutoCompSer(query_set, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# Search API for searching on the basis of title and description
def search_videos(request):
    query = request.GET.get("query")

    # Split the words on the basis of spaces to optimise the search for make tea => How to make tea
    query = list(query.split())
    stype = request.GET.get("type")
    q = Q()
    # If type is title we take the bitwise and with all the words containg the title, so it will give more optimised results
    if stype == "title":
        for term in query:
            q &= Q(title__icontains=term)
    # If type is description we take the bitwise and with all the words containg the description so it will give more optimised results   
    elif stype == "description":
        for term in query:
            q &= Q(description__icontains=term)
    # If type is title and description both, we take the bitwise and with all the words containg the title and then bitwise and with all the words containing description and then the bitwise or between two, so it will give more optimised results
    else:
        q1 = Q()
        q2 = Q()
        for term in query:
            q &= Q(title__icontains=term)
        for term in query:
            q &= Q(description__icontains=term)
        q |= q1
        q |= q2
        
    context = {
        "query": query,
        "videos": models.Video.objects.filter(q)[ 0:20 ],
    }
    videos = serializers.serialize("json", context["videos"])
    videos = json.loads(videos)
    return HttpResponse(json.dumps({"videos": videos}), content_type='application/json')