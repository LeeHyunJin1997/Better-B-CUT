from django.db import models
from better_b_cut import settings
from movie.models import Movie

# Create your models here.
class Adaptation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="adaptations")
    type = models.CharField(max_length=8)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class AdaptationLike(models.Model):
    adaptation = models.ForeignKey(Adaptation, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class AdaptationComment(models.Model):
    adaptation = models.ForeignKey(Adaptation, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class AdaptationCommentLike(models.Model):
    adaptation_comment = models.ForeignKey(AdaptationComment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)