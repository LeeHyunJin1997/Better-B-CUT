from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# password, is_active, last_login
class User(AbstractUser):
    nickname = models.CharField(max_length=8)
    signup_date = models.DateTimeField(auto_now_add=True)
    point = models.IntegerField()

    class Meta:
        db_table = 'user'

    # objects = CustomUserManager()