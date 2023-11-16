from rest_framework import serializers
from .models import Article,Comment
from accounts.serializers import UserSerializer

class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user','like_users')

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields='__all__'
        read_only_fields=('user','article','like_users')