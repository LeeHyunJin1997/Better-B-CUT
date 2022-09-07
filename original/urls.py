from django.contrib import admin
from django.urls import path
from . import views

app_name = "original"

urlpatterns = [
    path('', views.create_or_list_original, name="create_or_list_original"),
    path('<int:original_id>', views.original_detail, name="original_detail"),
    path('<int:original_id>/like', views.original_like, name="original_like"),
    path('<int:original_id>/comment', views.original_comment, name="original_comment"),
    path('<int:original_id>/comment/<int:original_comment_id>', views.original_comment_detail, name="original_comment_detail"),
    path('<int:original_id>/comment/<int:original_comment_id>/like', views.original_comment_like, name="original_comment_like"),
]
