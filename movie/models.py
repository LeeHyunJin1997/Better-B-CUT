from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=50)
    genre = models.CharField(max_length=16)
    poster = models.URLField(max_length=200)