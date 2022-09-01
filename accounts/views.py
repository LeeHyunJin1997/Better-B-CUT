from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import ProfileSerializer
# Create your views here.

User = get_user_model()

@api_view(['GET', 'PUT'])
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id):
    serializer = ProfileSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

def follow(request, user_id):
    pass