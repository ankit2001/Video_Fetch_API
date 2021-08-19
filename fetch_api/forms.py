from rest_framework import serializers

from . import models
from . import background_processes

class VideoSerializer(serializers.ModelSerializer):
    total_meta_data = serializers.SerializerMethodField()

    def get_total_meta_data(self, obj):
        return [VideoMetaDataSerializer(meta_data).data for meta_data in models.VideoMetaData.objects.filter(current_video=obj)]

    class Meta:
        model = models.Video
        fields = '__all__'
        read_only_fields = ('vid_id',)

class VideoMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VideoMetaData
        fields = '__all__'

class VideoAutoCompSer(serializers.ModelSerializer):
    class Meta:
        model = models.Video
        fields = ('vid_id', 'description', 'title',)