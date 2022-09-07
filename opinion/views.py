from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Opinion, OpinionLike, OpinionComment, OpinionCommentLike
from .serializers import OpinionSerializer, OpinionCommentSerializer
from movie.models import Movie
from movie.serializers import MovieSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def opinion_list(request):
    if request.method == 'GET':
        # 리스트 리턴
        opinion_list = Opinion.objects.all()
        opinion_list_serializer = OpinionSerializer(opinion_list, many=True)
        return Response(opinion_list_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        movie = request.data.get('movie')
        opinion_serializer = OpinionSerializer(data=request.data)
        movie_serializer = MovieSerializer(data=movie)

        # 로그인 여부 확인
        if request.user.is_authenticated:
            # 유효성 검사
            if opinion_serializer.is_valid(raise_exception=True):
                # 저장
                opinion_serializer.save(movie=movie, user=request.user)
                return Response(opinion_serializer.data, status=status.HTTP_201_CREATED)
        # 로그인 요구
        else:
            data = {
                'message': '로그인 후에 이용할 수 있습니다.'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'PUT', 'DELETE'])
def opinion_detail(request, opinion_id):
    opinion = get_object_or_404(Opinion, pk=opinion_id)
    if request.method == 'GET':
        serializer = OpinionSerializer(opinion)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        movie = get_object_or_404(Movie, pk=opinion.movie_id)
        serializer = OpinionSerializer(opinion, request.data)
        # 로그인 여부 확인
        if request.user.is_authenticated:
            # 동일 유저 확인
            if request.user == opinion.user:
                # 유효성 검사
                if serializer.is_valid(raise_exception=True):
                    # 저장
                    serializer.save(movie=movie, user=request.user)
                    # 리턴
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                data = {
                    'message': '수정은 작성자만 가능합니다.'
                }
                return Response(data, status.HTTP_403_FORBIDDEN)
        # 로그인 요구
        else:
            data = {
                'message': '로그인 후에 이용할 수 있습니다.'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'DELETE':
        # 로그인 여부 확인
        if request.user.is_authenticated:
            # 동일 유저 확인
            if request.user == opinion.user:
                # 삭제
                opinion.delete()
                data = {
                    'message': '정상적으로 삭제되었습니다.'
                }
                return Response(data, status=status.HTTP_204_NO_CONTENT)
            else:
                data = {
                    'message': '삭제는 작성자만 가능합니다.'
                }
                return Response(data, status=status.HTTP_403_FORBIDDEN)
        # 로그인 요구
        else:
            data = {
                'message': '로그인 후에 이용할 수 있습니다.'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST', 'DELETE'])
def like(request, opinion_id):
    opinion = get_object_or_404(Opinion, pk=opinion_id)
    # is_like = True >>> 좋아요
    opinion_like_user = OpinionLike.objects.filter(user=request.user, opinion=opinion, is_like=True).first()
    if request.method == 'POST':
        # 로그인 여부 확인
        if request.user.is_authenticated:
            # 좋아요가 이미 있다면
            if opinion_like_user:
                data = {
                    'message': '이미 좋아요 상태입니다.'
                }
                return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                # 갱신 후 리턴
                OpinionLike.objects.create(user=request.user, opinion=opinion, is_like=True)
                opinion = get_object_or_404(Opinion, pk=opinion_id)
                serializer = OpinionSerializer(opinion)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 로그인 요구
        else:
            data = {
                'message': '로그인 후에 이용할 수 있습니다.'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'DELETE':
        # 로그인 여부 확인
        if request.user.is_authenticated:
            # 좋아요가 있다면
            if opinion_like_user:
                # 삭제
                opinion_like_user.delete()
                # 갱신 후 리턴
                opinion = get_object_or_404(Opinion, pk=opinion_id)
                serializer = OpinionSerializer(opinion)
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
            else:
                data = {
                    'message': '아직 좋아요하지 않은 상태입니다.'
                }
                return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
        # 로그인 요구
        else:
            data = {
                'message': '로그인 후에 이용할 수 있습니다.'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST', 'DELETE'])
def dislike(request, opinion_id):
    opinion = get_object_or_404(Opinion, pk=opinion_id)
    # is_like = False >>> 싫어요
    opinion_dislike_user = OpinionLike.objects.filter(user=request.user, opinion=opinion, is_like=False).first()
    if request.method == 'POST':
        # 로그인 여부 확인
        if request.user.is_authenticated:
            # 싫어요가 이미 있다면
            if opinion_dislike_user:
                data = {
                    'message': '이미 싫어요 상태입니다.'
                }
                return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                # 갱신 후 리턴
                OpinionLike.objects.create(user=request.user, opinion=opinion, is_like=False)
                opinion = get_object_or_404(Opinion, pk=opinion_id)
                serializer = OpinionSerializer(opinion)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 로그인 요구
        else:
            data = {
                'message': '로그인 후에 이용할 수 있습니다.'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'DELETE':
        # 로그인 여부 확인
        if request.user.is_authenticated:
            # 싫어요가 있다면
            if opinion_dislike_user:
                # 삭제
                opinion_dislike_user.delete()
                # 갱신 후 리턴
                opinion = get_object_or_404(Opinion, pk=opinion_id)
                serializer = OpinionSerializer(opinion)
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
            else:
                data = {
                    'message': '아직 싫어요하지 않은 상태입니다.'
                }
                return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
        # 로그인 요구
        else:
            data = {
                'message': '로그인 후에 이용할 수 있습니다.'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
def comment_list(request, opinion_id):
    opinion = get_object_or_404(Opinion, pk=opinion_id)
    comments = get_list_or_404(OpinionComment, opinion=opinion)

    if request.method == 'GET':
        serializer = OpinionCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = OpinionCommentSerializer(data=request.data)
        # 로그인 여부 확인
        if request.user.is_authenticated:
            # 유효성 검사
            if serializer.is_valid(raise_exception=True):
                # 저장
                serializer.save(user=request.user, opinion=opinion)
                # 갱신 후 리턴
                comments = get_list_or_404(OpinionComment, opinion=opinion)
                serializer = OpinionCommentSerializer(comments, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 로그인 요구
        else:
            data = {
                'message': '로그인 후에 이용할 수 있습니다.'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT', 'DELETE'])
def comment_detail(request, opinion_id, opinion_comment_id):
    opinion = get_object_or_404(Opinion, pk=opinion_id)
    comment = get_object_or_404(OpinionComment, pk=opinion_comment_id)

    if request.method == 'PUT':
        # 로그인 여부 확인
        if request.user.is_authenticated:
            # 동일 유저 확인
            if request.user == comment.user:
                serializer =OpinionCommentSerializer(comment, data=request.data)
                # 유효성 검사
                if serializer.is_valid(raise_exception=True):
                    # 저장
                    serializer.save()
                    # 갱신 후 리턴
                    comments = get_list_or_404(OpinionComment, opinion=opinion)
                    serializer = OpinionCommentSerializer(comments, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                data = {
                    'message': '수정은 작성자만 가능합니다.'
                }
                return Response(data, status=status.HTTP_403_FORBIDDEN)
        # 로그인 요구
        else:
            data = {
                'message': '로그인 후에 이용할 수 있습니다.'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
    
    elif request.method == 'DELETE':
        # 로그인 여부 확인
        if request.user.is_authenticated:
            # 동일 유저 확인
            if request.user == comment.user:
                # 삭제
                comment.delete()
                # 갱신 후 리턴
                comments = get_list_or_404(OpinionComment, opinion=opinion)
                serializer = OpinionCommentSerializer(comments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                data = {
                    'message': '삭제는 작성자만 가능합니다.'
                }
                return Response(data, status=status.HTTP_403_FORBIDDEN)
        # 로그인 요구
        else:
            data = {
                'message': '로그인 후에 이용할 수 있습니다.'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST', 'DELETE'])
def comment_like(request, opinion_comment_id):
    comment = get_object_or_404(OpinionComment, pk=opinion_comment_id)
    opinion_comment_like_user = OpinionCommentLike.objects.filter(user=request.user, comment=comment).first()

    if request.method == 'POST':
        # 로그인 여부 확인
        if request.user.is_authenticated:
            # 좋아요가 이미 있다면
            if opinion_comment_like_user:
                data = {
                    'message': '이미 좋아요 상태입니다.'
                }
                return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                # 저장
                OpinionCommentLike.objects.create(user=request.user, comment=comment)
                # 갱신 후 리턴
                comment = get_object_or_404(OpinionComment, pk=opinion_comment_id)
                serializer = OpinionCommentSerializer(comment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 로그인 요구
        else:
            data = {
                'message': '로그인 후에 이용할 수 있습니다.'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'DELETE':
        # 로그인 여부 확인
        if request.user.is_authenticated:
            # 좋아요가 있다면
            if opinion_comment_like_user:
                # 삭제
                opinion_comment_like_user.delete()
                # 갱신 후 리턴
                comment = get_object_or_404(OpinionComment, pk=opinion_comment_id)
                serializer = OpinionCommentSerializer(comment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                data = {
                    'message': '아직 좋아요하지 않은 상태입니다.'
                }
                return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
        # 로그인 요구
        else:
            data = {
                'message': '로그인 후에 이용할 수 있습니다.'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)