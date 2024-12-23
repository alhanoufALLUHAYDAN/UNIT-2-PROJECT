from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    replied = models.BooleanField(default=False)  

    
