from django.shortcuts import render
from .models import Movie
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MovieSerializer

# Create your views here.
@api_view(['POST'])
def search_movie(request, movie_id):
    if Movie.objects.filter(id=movie_id).exists():
        data = {
            'message': '해당 영화는 이미 DB에 존재합니다.',
            'movie_id': movie_id
        }
        return Response(data, status=status.HTTP_208)
    else:
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
