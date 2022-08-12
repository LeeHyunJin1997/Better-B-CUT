from django.db import models
from django.conf import settings

# Create your models here.
class Original(models.Model):
    ARTICLE_TYPES = (
        ('Story', '시나리오'),
        ('Script', '대본'),
    )

    # writer
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='originals')

    type = models.CharField(max_length=8, choices=ARTICLE_TYPES)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class OriginalLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    original = models.ForeignKey(Original, on_delete=models.CASCADE, related_name='original_likes')


class OriginalComment(models.Model):
    # original
    original = models.ForeignKey(Original, on_delete=models.CASCADE)
    # writer
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='original_comments')

    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class OriginalCommentLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    original_comment = models.ForeignKey(OriginalComment, on_delete=models.CASCADE, related_name='original_comment_likes')