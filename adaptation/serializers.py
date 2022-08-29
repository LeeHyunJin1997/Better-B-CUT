from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Adaptation, AdaptationLike, AdaptationComment, AdaptationCommentLike
from ..movie.serializers import MovieSerializer

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ('nickname', )


class AdaptationListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()


    class Meta:
        model = Adaptation
        fields = '__all__'


    def get_like_count(self, instance):
        data = AdaptationLike.objects.filter(adaptation__id=instance.id).count()
        return data


class AdaptationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    now_like = serializers.SerializerMethodField()


    class Meta:
        model = Adaptation
        fields = '__all__'


    def get_like_count(self, instance):
        data = AdaptationLike.objects.filter(adaptation_id=instance.id).count()
        return data


    def get_now_like(self, instance):
        data = AdaptationLike.objects.filter(adaptation_id=instance.id, user_id=instance.user.id).exists()
        return data


class AdaptationCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    adaptation = AdaptationSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    now_like = serializers.SerializerMethodField()


    class Meta:
        model = AdaptationComment
        fields = '__all__'

    
    def get_like_count(self, instance):
        data = AdaptationCommentLike.objects.filter(adaptation_comment_id=instance.id).count()
        return data


    def get_now_like(self, instance):
        data = AdaptationCommentLike.objects.filter(adaptation_comment_id=instance.id, user_id=instance.user.id).exists()
        return data

    

        
