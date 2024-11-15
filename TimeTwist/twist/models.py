from django.db import models

# Create your models here.

class TimeTwist(models.Model):

    entry_type_choices = [
    ('Article', 'Article'),
    ('Experience', 'Experience'),
    ]

    title = models.CharField(max_length=1024)
    content = models.TextField()
    entry_type = models.CharField(max_length=255, choices=entry_type_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True) 

    def __str__(self):
         return self.title
