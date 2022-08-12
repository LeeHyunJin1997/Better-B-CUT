from django.db import models
from django.conf import settings

# Create your models here.
class Original(models.Model):
    # writer
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='originals')

    article_type = models.CharField(max_length=8)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_originals')

    def __str__(self):
        return self.title

class OriginalComment(models.Model):
    # original
    original = models.ForeignKey(Original, on_delete=models.CASCADE)
    # writer
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='original_comments')

    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_original_comments')