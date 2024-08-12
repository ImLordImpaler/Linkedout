from rest_framework.serializers import ModelSerializer
from .models import Post, PostReaction, PostComment, Connection
import json 


class ConnectionSerializer(ModelSerializer):
    class Meta:
        model = Connection
        fields = ['id', 'user_from','user_to', 'created_at', 'updated_at']
        
class CommentSerializer(ModelSerializer):
    class Meta:
        model = PostComment
        fields = ['id','user', 'post', 'post_comment']


class PostReactionSerializer(ModelSerializer):
    class Meta:
        model = PostReaction
        fields = ['id','post', 'user', 'reaction_type']


class PostSerializer(ModelSerializer):
    post_reaction = PostReactionSerializer(many=True, read_only=True)
    post_comments = CommentSerializer(many=True , read_only=True)
    class Meta:
        model = Post
        fields =  ['id','post_comments', 'user_id', 'post_data', 'reaction_count', 'comment_count', 'post_reaction']
