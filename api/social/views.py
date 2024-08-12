from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

import social.models as social_models 
import accounts.models as account_models
from social.serializers import PostSerializer, PostReactionSerializer, CommentSerializer, ConnectionSerializer


class PostView(ViewSet):

    def __init__(self):
        self.post_filter = {}  # Pass this as filters for posts. 
        self.post_return_values = []

        self.create_post_data = {}

    def get_post(self , request, pk):
        try:
            post = social_models.Post.objects.get(id =pk)
            postSerial = PostSerializer(post, many=False)

            return Response(data={'data': postSerial.data}, status=200)
        except social_models.Post.DoesNotExist as E:
            return Response(data={'error_message': "Post Doesn't exist"}, status=401) 
        except Exception as E:
            return Response(data={'error_message': str(E)}, status=401)
        
    def show_posts(self , request):   
        params = request.data
        filters = self.filter_post(params)
        posts = social_models.Post.objects.\
                    filter(**filters).\
                    values(*self.post_return_values)
        
        postSerial = PostSerializer(posts, many=True)
        return Response(data = postSerial.data, status=200)
    

    def filter_post(self , params):
        '''
        Write Logic for Posts Filters.
        '''
        return params
    

    def create_post(self, request, *args, **kwargs):
        try:
            valid_post_data = self.validate_post_data(request.data['post_data'])
            
            post = social_models.Post.objects.create(
                user_id = request.user_id, 
                post_data = valid_post_data
            )
            post = PostSerializer(post)
            return Response(data={'message': post.data}, status=200)
        except KeyError as E:
            return Response(data={'error_message': "Please Pass the missing fields {}".format(str(E))}, status=401)
        except Exception as E:
            return Response(data={'error_message': str(E)}, status=401)
    
    def validate_post_data(self , data):
        # Validate Post Required data over here. 
        return data 
    

    def delete_post(self, request , pk):
        try:
            post = social_models.Post.objects.get(id =pk)
            print(post.id)
            post.delete()
            
            return Response(data={'data': "Post Deleted!"}, status=200)
        except social_models.Post.DoesNotExist as E:
            return Response(data={'error_message': "Post Doesn't exist"}, status=401) 
        except Exception as E:
            return Response(data={'error_message': str(E)}, status=401)
        

class Interaction(ViewSet):

    def __init__(self):
        self.reaction_data = {}
        self.comment_data = {}

    def delete_connection(self , request):
        try:
            from_user = request.data['from']
            to_user = request.data['to']

            connection = social_models.Connection.objects.get(user_from = from_user, user_to = to_user).delete()
            return Response('{} Removed {}'.format(from_user, to_user))
        except Exception as E:
            return Response(data = str(E), status=400)

    def get_connections(self , request):
        try:
            params = {} # Try to fill this for filters?

            connections = social_models.Connection.objects.filter(**params)
            serial = ConnectionSerializer(connections, many=True)
            return Response(data=serial.data , status=200)
        except Exception as E:
            return Response(data = str(E), status=400)
        
    def create_connection(self , request):
        try:
            from_user = request.data['from']
            to_user = request.data['to']

            connection = social_models.Connection.objects.create(user_from_id = from_user, user_to_id = to_user) 

            return Response(data="{} Added {}".format(from_user , to_user), status=201)
        except Exception as E:
            return Response(data={'error_message':str(E)}) 

    def get_comment(self, request , pk):
        try:
            comment = social_models.PostComment.objects.get(id = pk)
            serial = CommentSerializer(comment)
            return Response(data={'data':serial.data}, status=200)
        except Exception as E:
            return Response(data={'error':str(E)}, status=400)
        
    def delete_comment(self , request, pk):
        comment = social_models.PostComment.objects.get(id=pk).delete()
        return Response(data={'data':"Deleted"}, status=200)
    

    def create_reaction(self, request):
        try:
            reaction_type = request.data['reaction_type']
            if reaction_type not in social_models.PostReaction.REACTION_TYPE.keys():
                raise Exception("Invalid Reaction Type")
            
            self.reaction_data = {
                'reaction_type': reaction_type,
                'post_id': request.data['post_id'],
                'user_id': request.user_id
            }

            existing_reaction = social_models.PostReaction.objects.filter(**self.reaction_data)
            print(existing_reaction)
            if existing_reaction:
                reaction = existing_reaction.delete()
                return Response(data={'data':"Removed {} reaction from {}".format(reaction_type, request.data['post_id'])}, status=201)
            else:
                new_reaction = social_models.PostReaction.objects.create(**self.reaction_data)
            
            
            return Response(data={'data':"Reacted {} to {}".format(reaction_type, request.data['post_id'])}, status=200)
        except KeyError as E:
            return Response(data={"error_message": "Please Provide {}".format(str(E))} , status =400)
        except Exception as E:
            return Response(data={'error_message': str(E)}, status=401)
        

    def create_comment(self, request):
        try:
            
            self.comment_data = {
                'post': request.data['post_id'],
                'user': request.user_id, 
                'post_comment': request.data['post_comment']
            }

            serial = CommentSerializer(data = self.comment_data)
            print(serial.is_valid())
            if serial.is_valid(raise_exception=True):
                print(serial.error_messages)
                serial.save() 

            return Response(data={'data':serial.data}, status=200)
        except KeyError as E:
            return Response(data={"error_message": "Please Provide {}".format(str(E))} , status =400)
        except Exception as E:
            return Response(data={'error_message': str(E)}, status=401)
