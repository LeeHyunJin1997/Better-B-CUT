from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Opinion, OpinionLike, OpinionComment, OpinionCommentLike
from ..movie.serializers import MovieSerializer

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ('nickname', )


class OpinionListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()


    class Meta:
        model = Opinion
        fields = '__all__'


    def get_like_count(self, instance):
        data = OpinionLike.objects.filter(opinion_id=instance.id).count()
        return data


class OpinionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    now_like = serializers.SerializerMethodField()


    class Meta:
        model = Opinion
        fields = '__all__'


    def get_like_count(self, instance):
        data = Opinion.objects.filter(opinion_id=instance.id).count()
        return data


    def get_now_like(self, instance):
        data = Opinion.objects.filter(opinion_id=instance.id, user_id=instance.user.id).exists()
        return data


class OpinionCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    adaptation = OpinionSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    now_like = serializers.SerializerMethodField()


    class Meta:
        model = OpinionComment
        fields = '__all__'

    
    def get_like_count(self, instance):
        data = OpinionCommentLike.objects.filter(opinion_comment_id=instance.id).count()
        return data


    def get_now_like(self, instance):
        data = OpinionCommentLike.objects.filter(opinion_comment_id=instance.id, user_id=instance.user.id).exists()
        return data
