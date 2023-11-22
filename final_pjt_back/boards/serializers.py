from rest_framework import serializers
from .models import Article,Comment
from accounts.serializers import UserSerializer,CustomUserDetailSerializer

class ArticleSerializer(serializers.ModelSerializer):
    user = CustomUserDetailSerializer(read_only=True)
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user','like_users')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user, context=self.context).data
        return representation

class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserDetailSerializer(read_only=True)
    class Meta:
        model = Comment
        fields='__all__'
        read_only_fields=('user','article','like_users')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user, context=self.context).data
        return representation