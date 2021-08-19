from django.contrib import admin

from . import models

@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
	list_display = [field.name for field in models.Video._meta.fields]
	search_fields = ('published_at', 'vid_id', 'title', 'description'),
	list_filter = ('published_at', 'title', 'description')


@admin.register(models.VideoMetaData)
class VideoThumbNailAdmin(admin.ModelAdmin):
	list_display = [field.name for field in models.VideoMetaData._meta.fields]
	search_fields = ('video__title', 'video__vid_id', 'video__published_at', 'video__description')
	list_filter = ('current_video', 'thumbnail_size')

