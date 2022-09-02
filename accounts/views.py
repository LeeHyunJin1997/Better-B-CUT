from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import ProfileSerializer
from .models import Follow
from django.contrib.auth.decorators import login_required
# Create your views here.

User = get_user_model()

@api_view(['GET', 'PUT'])
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id):
    serializer = ProfileSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@login_required
@api_view(['POST'])
def follow(request, user_id):
    user = request.user
    follow_user = User.objects.filter(id=user_id)
    if user.is_authenticated:
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