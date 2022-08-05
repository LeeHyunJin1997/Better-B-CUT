from email import contentmanager
from turtle import title
from django.db import models

# Create your models here.
class Original(models.Model):
    article_type = models.CharField(max_length=8)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)