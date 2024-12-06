from rest_framework import serializers
from django.contrib.auth import get_user_model
from articles.models import Article, Tag
from profiles.models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ['user']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name',]

class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = ProfileSerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 
            'title', 
            'tags', 
            'created_at', 
            'author', 
            'likes', 
            'dislikes',
        ]

class SingleArticleSerializer(ArticleSerializer):
    class Meta:
        model = Article
        fields = [
            'id', 
            'title',
            'content', 
            'tags', 
            'created_at', 
            'author', 
            'likes', 
            'dislikes',
        ]