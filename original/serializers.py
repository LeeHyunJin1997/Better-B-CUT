from rest_framework import serializers
from .models import Original, OriginalComment

class OriginalListSerializer(serializers.Serializer):

    class Meta:
        model = Original
        fields = '__all__'
        read_only_fields = ('user', )

class OriginalSerializer(serializers.Serializer):

    class Meta:
        model = Original
        fields = '__all__'

class OriginalCommentSeirializer(serializers.Serializer):

    class Meta:
        model = OriginalComment
        fields = '__all__'