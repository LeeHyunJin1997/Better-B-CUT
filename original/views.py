from django.shortcuts import render
from rest_framework.decorators import api_view
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from movie.models import Movie
from original.models import Original, OriginalLike
from original.serializers import OriginalLikeSerializer, OriginalListSerializer, OriginalSerializer

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
    original = get_object_or_404(Original, id=original_id)
    if request.method == 'GET':
        serializer = OriginalSerializer(original)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = OriginalSerializer(original, data=request.data)
        if original.user == request.user:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, stauts=status.HTTP_201_CREATED)
        else:
            data = {
                'message': '수정은 작성자만 가능합니다.'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'DELETE':
        if original.user == request.user:
            original.delete()
            data = {
                'message': '정상적으로 삭제되었습니다.'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        else:
            data = {
                'message': '삭제는 작성자만 가능합니다.'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'POST', 'DELETE'])
def original_like(request, original_id):
    original = get_object_or_404(Original, id=original_id)
    user = request.user
    if request.method == 'GET':
        like_users = get_list_or_404(OriginalLike, original=original)
        serializer = OriginalLikeSerializer(like_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if OriginalLike.objects.filter(user=user, original=original).exists():
            data = {
                'message': '이미 좋아요 상태입니다.'
            }
            return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            serializer=OriginalSerializer(data=request.data)
            serializer.save(user=user, original=original)

            like_users = get_list_or_404(OriginalLike, original=original)
            serializer = OriginalLikeSerializer(like_users, many=True)
            return Response(serializer.data, staus=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        if OriginalLike.objects.filter(user=user, original=original).exists():
            original_like = OriginalLike.objects.filter(user=user, original=original)
            original_like.delete()

            like_users = get_list_or_404(OriginalLike, original=original)
            serializer = OriginalLikeSerializer(like_users, many=True)
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'message': '좋아요 하지 않은 상태입니다.'
            }
            return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)

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
