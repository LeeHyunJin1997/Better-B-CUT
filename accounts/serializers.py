from rest_framework import serializers
from adaptation.serializers import AdaptationListSerializer
from opinion.serializers import OpinionListSerializer
from original.serializers import OriginalListSerializer
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class FollowListSerializer(serializers.ModelSerializer):

        class Meta: 
            model = get_user_model()
            fields = ('pk', 'nickname',)
    
    adaptations = AdaptationListSerializer(many=True)
    opinion_set = OpinionListSerializer(many=True)
    originals = OriginalListSerializer(many=True)
    to_user = FollowListSerializer(many=True)
    from_user = FollowListSerializer(many=True)
    

    class Meta:
        model = get_user_model()
        fields = ('pk', 'nickname', 'point', 'adaptations', 'opinion_set', 'originals', 'to_user', 'from_user',)