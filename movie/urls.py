from django.urls import path
from . import views

app_name = "movie"

urlpatterns = [
    path('/movie_id', views.search_movie, name="serach_movie"),
]