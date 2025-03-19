from rest_framework import serializers
from .models import Post, Like, Comment
from drf_spectacular.utils import extend_schema_field

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.email")  
    likes_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField() 
    @extend_schema_field(serializers.IntegerField())
    def get_likes_count(self, obj):
        return obj.likes.count()
    def get_comments(self, obj):  
        comments = obj.comments.all()  
        return CommentSerializer(comments, many=True).data 
    class Meta:
        model = Post
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "post"]

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")  

    class Meta:
        model = Comment
        fields = ["id", "user", "post", "content", "created_at"]


class LikeStatusSerializer(serializers.Serializer):
    message = serializers.CharField()
