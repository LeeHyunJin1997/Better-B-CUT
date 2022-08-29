from django.shortcuts import render
from rest_framework.decorators import api_view
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from movie.models import Movie
from original.models import Original, OriginalComment, OriginalCommentLike, OriginalLike
from original.serializers import OriginalCommentLikeSerializer, OriginalCommentSerializer, OriginalLikeSerializer, OriginalListSerializer, OriginalSerializer

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

@api_view(['POST', 'DELETE'])
def original_like(request, original_id):
    original = get_object_or_404(Original, id=original_id)
    user = request.user

    if request.method == 'POST':
        if OriginalLike.objects.filter(user=user, original=original).exists():
            data = {
                'message': '이미 좋아요 상태입니다.'
            }
            return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            OriginalLike.objects.create(user=user, original=original)

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

@api_view(['GET', 'POST'])
def original_comment(request, original_id):
    original = get_object_or_404(Original, id=original_id)
    comments = get_list_or_404(OriginalComment, original=original)

    if request.method == 'GET':
        serializer = OriginalCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = OriginalCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, original=original)

            comments = OriginalComment.objects.all()
            serializer = OriginalCommentSerializer(comments, many=True)
            #댓글 리스트가 있고 상세보기가 따로 있나??
            return Response(serializer.data, stastus=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
def original_comment_detail(request, original_id, original_comment_id):
    comment = get_object_or_404(OriginalComment, id=original_comment_id)
    if request.method == 'PUT':
        if comment.user == request.user:
            serializer = OriginalCommentSerializer(comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                comments = OriginalComment.objects.all()
                serializer = OriginalCommentSerializer(comments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = {
                'message': '댓글은 작성자만 수정 가능합니다.'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'DELETE':
        if comment.user == request.user:
            comment.delete()

            comments = OriginalComment.objects.all()
            serializer = OriginalCommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            data = {
                'message': '댓글은 작성자만 삭제 가능합니다.'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'DELETE'])
def original_comment_like(request, original_id, original_comment_id):
    original = get_object_or_404(Original, id=original_id)
    comment = get_object_or_404(OriginalComment, id=original_comment_id)
    user = request.user

    if request.method == 'POST':
        if OriginalCommentLike.objects.filter(user=user, original_comment=comment).exists():
            data = {
                'messsage': '이미 좋아요 한 상태입니다.'
            }
            return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            OriginalCommentLike.objects.create(user=user, original_comment=comment)
            like_users = get_list_or_404(OriginalCommentLike, original_comment=comment)
            serializer = OriginalCommentLikeSerializer(like_users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        if not OriginalCommentLike.objects.filter(user=user, original_comment=comment).exists():
            data = {
                'messsage': '이미 좋아요 하지 않은 상태입니다.'
            }
            return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            original_comment_like = OriginalCommentLike.objects.filter(user=user, original_comment=comment)
            original_comment_like.delete()

            like_users = get_list_or_404(OriginalCommentLike, original_comment=comment)
            serializer = OriginalCommentLikeSerializer(like_users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            