from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import ProfileSerializer, UserSerializer
from .models import Follow
from django.contrib.auth.decorators import login_required
# Create your views here.

User = get_user_model()

@api_view(['GET', 'PUT'])
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'GET':
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        if request.user.is_authenticated:
            if request.user == user:
                serializer = UserSerializer(user, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                data = {
                    'message': '본인의 정보만 수정할 수 있습니다.'
                }
                return Response(data, status=status.HTTP_403_FORBIDDEN)
        else:
            data = {
                'message': '로그인이 필요합니다.'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        


@login_required
@api_view(['POST'])
def follow(request, user_id):
    user = request.user
    follow_user = User.objects.filter(id=user_id)
    #이미 팔로우 한 경우
    if Follow.objects.filter(from_user=user, to_user=follow_user).exists():
        follow = Follow.objects.filter(from_user=user, to_user=follow_user)
        follow.delete()
        data = {
            'message': '팔로우가 취소되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    else:
        Follow.objects.create(from_user=user, to_user=follow_user)
        data = {
            'message': '팔로우 되었습니다.'
        }
        return Response(data, status=status.HTTP_201_CREATED)