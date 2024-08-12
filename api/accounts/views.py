from django.contrib.auth import authenticate 
from django.contrib.auth.models import User

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

import accounts.models as accounts_models 
from .serializers import UserSerializer

class Auth(ViewSet):

    def logout(self , request):
        user_id = accounts_models.UserProfile.objects.get(id = request.user_id).user_id
        
        Token.objects.get(user_id = user_id).delete()

        return Response(data="Logged Out!", status=201) 

    def register(self , request):
        """
        Input: username , password1 , password2 , email
        Output: 
        {   
            "id":1
            "username":"",
            "email":"",
            "":""
        }
        """
        try:
            username = request.data['username']
            password1 = request.data['password1']
            password2 = request.data['password2']
            email = request.data['email']

            if password1 != password2:
                raise Exception("Password Doesn't match")
            
            user = User.objects.create_user(
                username=username,
                password=password1,
                email=email
            )
            token = Token.objects.create(user=user)
            
            return Response(data={'username':username , 'token':"Token {}".format(token.key)}, status=200)
        except KeyError as e:
            return Response(data={'error':str(e)}, status=401) 
        
    
    def login(self , request):
        try:
            username=request.data['username']
            password=request.data['password']

            user = authenticate(request=request,username=username,password=password)
            if not user:
                raise Exception("Incorrect Username Password Combination")
            
            token,created = Token.objects.get_or_create(user=user)
            return Response(data={
                "username":username,
                "token":"Token {}".format(token.key)
            }, status=200)
        except Exception as E:
            return Response(data={
                "error":str(E)
            }, status=401)
        

class UserView(ViewSet):

    def get_users(self , request):
        users = accounts_models.UserProfile.objects.all() 

        serial = UserSerializer(users, many=True)

        return Response(data=serial.data, status=200)