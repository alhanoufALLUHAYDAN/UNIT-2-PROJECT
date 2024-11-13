from django.db import models

# Create your models here.

class TimeTwist(models.Model):

    title = models.CharField(max_length=1024)
    content = models.TextField()
    entry_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)