from django.db import models
from better_b_cut import settings
from movie.models import Movie

# Create your models here.
class Opinion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='opinions')
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    img = models.ImageField(upload_to='media/', blank=True, null=True)

class OpinionLike(models.Model):
    opinion = models.ForeignKey(Opinion, on_delete=models.CASCADE, related_name='opinion_like')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='like_opinion')
    is_like = models.BooleanField(null=True)

class OpinionComment(models.Model):
    opinion = models.ForeignKey(Opinion, on_delete=models.CASCADE, related_name='opinion_comment')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class OpinionCommentLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    opinion_comment = models.ForeignKey(OpinionComment, on_delete=models.CASCADE, related_name='comment_like')