# middleware.py
from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract token and attach user to request
        auth_header = get_authorization_header(request).decode('utf-8')
        token_key = None

        print('\n MIDDLEWARE EXECUTED \n')

        if auth_header and auth_header.startswith('Token '):
            token_key = auth_header.split(' ')[1]

        if token_key:
            try:
                token = Token.objects.get(key=token_key)
                print('token!', token)
                request.user = token.user
            except Token.DoesNotExist:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()

        # Call the view
        response = self.get_response(request)
        return response
