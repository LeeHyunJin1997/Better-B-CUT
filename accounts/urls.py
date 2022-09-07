from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('profile/<int:user_id>', views.profile, name="profile"),
    path('follow/<int:user_id>', views.follow, name="follow"),
]
