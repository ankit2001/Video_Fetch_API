from django.db import models

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=450)
    vid_id = models.CharField(max_length=150, unique=True)
    description = models.CharField(max_length=2000)
    published_at = models.DateTimeField(auto_now_add=True, db_index=True)
    class Meta:
        indexes = [
            models.Index(fields=['-published_at']),
        ]
    def __str__(self):
        return self.title

    

class VideMetaData(models.Model):

    current_video = models.ForeignKey(Video, on_delete=models.CASCADE)
    thumbnail_size = models.CharField(max_length=150)
    thumbnail_url =  models.CharField(max_length=450)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.video.title
