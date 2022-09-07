from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Adaptation, AdaptationLike, AdaptationComment, AdaptationCommentLike
from .serializers import AdaptationSerializer, AdaptationCommentSerializer
from ..movie.models import Movie
from ..movie.serializers import MovieSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def adaptation_list(request):
    if request.method == 'GET':
        # 리스트 리턴
        adaptation_list = Adaptation.objects.all()
        adaptation_list_serializer = AdaptationSerializer(adaptation_list, many=True)
        return Response(adaptation_list_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        movie = request.data.get('movie')
        adaptation_serializer = AdaptationSerializer(data=request.data)
        movie_serializer = MovieSerializer(data=movie)

        # 로그인 여부 확인
        if request.user.is_authenticated:
            # 유효성 검사
            if adaptation_serializer.is_valid(raise_exception=True):
                # 저장
                adaptation_serializer.save(movie=movie, user=request.user)
                return Response(adaptation_serializer.data, status=status.HTTP_201_CREATED)
        # 로그인 요구
        else:
            data = {
                'message': '로그인 후에 이용할 수 있습니다.'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'PUT', 'DELETE'])
def adaptation_detail(request, adaptation_id):
    adaptation = get_object_or_404(Adaptation, pk=adaptation_id)
    if request.method == 'GET':
        serializer = AdaptationSerializer(adaptation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        movie = get_object_or_404(Movie, pk=adaptation.movie_id)
        serializer = AdaptationSerializer(adaptation, request.data)
        # 로그인 여부 확인
        if request.user.is_authenticated:
            # 동일 유저 확인
            if request.user == adaptation.user:
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
            if request.user == adaptation.user:
                # 삭제
                adaptation.delete()
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
def like(request, adaptation_id):
    adaptation = get_object_or_404(Adaptation, pk=adaptation_id)
    adaptation_like_user = AdaptationLike.objects.filter(user=request.user, adaptation=adaptation).first()
    if request.method == 'POST':
        # 로그인 여부 확인
        if request.user.is_authenticated:
            # 좋아요가 이미 있다면
            if adaptation_like_user:
                data = {
                    'message': '이미 좋아요 상태입니다.'
                }
                return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                # 갱신 후 리턴
                AdaptationLike.objects.create(user=request.user, adaptation=adaptation)
                adaptation = get_object_or_404(Adaptation, pk=adaptation_id)
                serializer = AdaptationSerializer(adaptation)
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
            if adaptation_like_user:
                # 삭제
                adaptation_like_user.delete()
                # 갱신 후 리턴
                adaptation = get_object_or_404(Adaptation, pk=adaptation_id)
                serializer = AdaptationSerializer(adaptation)
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


@api_view(['GET', 'POST'])
def comment_list(request, adaptation_id):
    adaptation = get_object_or_404(Adaptation, pk=adaptation_id)
    comments = get_list_or_404(AdaptationComment, adaptation=adaptation)

    if request.method == 'GET':
        serializer = AdaptationCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = AdaptationCommentSerializer(data=request.data)
        # 로그인 여부 확인
        if request.user.is_authenticated:
            # 유효성 검사
            if serializer.is_valid(raise_exception=True):
                # 저장
                serializer.save(user=request.user, adaptation=adaptation)
                # 갱신 후 리턴
                comments = get_list_or_404(AdaptationComment, adaptation=adaptation)
                serializer = AdaptationCommentSerializer(comments, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 로그인 요구
        else:
            data = {
                'message': '로그인 후에 이용할 수 있습니다.'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT', 'DELETE'])
def comment_detail(request, adaptation_id, adaptation_comment_id):
    adaptation = get_object_or_404(Adaptation, pk=adaptation_id)
    comment = get_object_or_404(AdaptationComment, pk=adaptation_comment_id)

    if request.method == 'PUT':
        # 로그인 여부 확인
        if request.user.is_authenticated:
            # 동일 유저 확인
            if request.user == comment.user:
                serializer =AdaptationCommentSerializer(comment, data=request.data)
                # 유효성 검사
                if serializer.is_valid(raise_exception=True):
                    # 저장
                    serializer.save()
                    # 갱신 후 리턴
                    comments = get_list_or_404(AdaptationComment, adaptation=adaptation)
                    serializer = AdaptationCommentSerializer(comments, many=True)
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
                comments = get_list_or_404(AdaptationComment, adaptation=adaptation)
                serializer = AdaptationCommentSerializer(comments, many=True)
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
def comment_like(request, adaptation_comment_id):
    comment = get_object_or_404(AdaptationComment, pk=adaptation_comment_id)
    adaptation_comment_like_user = AdaptationCommentLike.objects.filter(user=request.user, comment=comment).first()

    if request.method == 'POST':
        # 로그인 여부 확인
        if request.user.is_authenticated:
            # 좋아요가 이미 있다면
            if adaptation_comment_like_user:
                data = {
                    'message': '이미 좋아요 상태입니다.'
                }
                return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                # 저장
                AdaptationCommentLike.objects.create(user=request.user, comment=comment)
                # 갱신 후 리턴
                comment = get_object_or_404(AdaptationComment, pk=adaptation_comment_id)
                serializer = AdaptationCommentSerializer(comment)
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
            if adaptation_comment_like_user:
                # 삭제
                adaptation_comment_like_user.delete()
                # 갱신 후 리턴
                comment = get_object_or_404(AdaptationComment, pk=adaptation_comment_id)
                serializer = AdaptationCommentSerializer(comment)
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
