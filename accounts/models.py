from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=8)
    signup_date = models.DateTimeField(auto_now_add=True)
    point = models.IntegerField(null=True)


    class Meta:
        db_table = 'user'


class Follow(models.Model):
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='to_user')
    to_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='from_user')

    class Meta:
        db_table = 'follow'