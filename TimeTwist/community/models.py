from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class CommunityPost(models.Model):
    title = models.CharField(max_length=1024)  
    content = models.TextField()  
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")  
    created_at = models.DateTimeField(auto_now_add=True)  
    
    def __str__(self):
        return f"{self.title} by {self.creator.username}"

class CommunityComment(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name="comments") 
    content = models.TextField() 
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")  
    created_at = models.DateTimeField(auto_now_add=True) 
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"Comment by {self.creator.username} on {self.post.title}"

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    comment = models.ForeignKey(CommunityComment, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username} on {self.comment.post.title}"