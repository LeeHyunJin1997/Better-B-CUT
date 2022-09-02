from rest_framework import serializers
from .models import Original, OriginalComment, OriginalCommentLike, OriginalLike

class OriginalListSerializer(serializers.Serializer):

    class Meta:
        model = Original
        fields = '__all__'
        read_only_fields = ('user', )

class OriginalSerializer(serializers.Serializer):

    class Meta:
        model = Original
        fields = '__all__'

class OriginalCommentSerializer(serializers.Serializer):

    class Meta:
        model = OriginalComment
        fields = '__all__'

class OriginalLikeSerializer(serializers.Serializer):

    class Meta:
        model = OriginalLike
        fields = '__all__'

class OriginalCommentLikeSerializer(serializers.Serializer):

    class Meta:
        model = OriginalCommentLike
        fields = '__all__'
        read_only_fields = '__all__'