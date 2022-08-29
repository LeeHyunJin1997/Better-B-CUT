from django.shortcuts import render
from rest_framework.decorators import api_view
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from movie.models import Movie
from original.models import Original
from original.serializers import OriginalListSerializer, OriginalSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def create_or_list_original(request):
    if request.method == 'GET':
        originals = Original.objects.all()
        serializer = OriginalListSerializer(originals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = OriginalSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def original_detail(request, original_id):
    if request.method == 'GET':
        pass
    
    elif request.method == 'PUT':
        pass

    elif request.method == 'DELETE':
        pass

@api_view(['GET', 'POST', 'DELETE'])
def original_like(request, original_id):
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        pass

    elif request.method == 'DELETE':
        pass

@api_view(['GET', 'POST']):
def original_comment(request, original_id):
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        pass

@api_view(['PUT', 'DELETE']):
def original_comment_detail(request, original_id, original_comment_id):
    if request.method == 'PUT':
        pass

    elif request.method == 'DELETE':
        pass

@api_view(['GET', 'POST', 'DELETE'])
def original_comment_like(request, originanl_id, original_comment_id):
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        pass

    elif request.method == 'DELETE':
        pass
