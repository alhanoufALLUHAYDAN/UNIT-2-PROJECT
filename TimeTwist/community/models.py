from django.db import models

# Create your models here.


class CommunityPost(models.Model):

    title = models.CharField(max_length=1024)
    content = models.TextField()
    creator = models.ForeignKey()
    created_at = models.DateTimeField(auto_now_add=True)


class CommunityComment(models.Model):

    post = models.ForeignKey(CommunityPost)
    content = models.TextField()
    creator = models.ForeignKey()
    created_at = models.DateTimeField(auto_now_add=True)