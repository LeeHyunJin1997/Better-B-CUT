from django.shortcuts import render
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET', 'POST'])
def opinion_list(request):
    pass


@api_view(['GET', 'PUT', 'DELETE'])
def opinion_detail(request):
    pass


@api_view(['GET', 'POST', 'DELETE'])
def like(request):
    pass


@api_view(['GET', 'POST', 'DELETE'])
def dislike(request):
    pass


@api_view(['GET', 'POST'])
def comment_list(request):
    pass


@api_view(['PUT', 'DELETE'])
def comment_detail(request):
    pass


@api_view(['GET', 'POST', 'DELETE'])
def comment_like(request):
    pass