from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.conf import settings
from accounts.models import UserProfile

class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        print(request.path)

        excluded_paths = [
            '/accounts/register',
            '/accounts/login',
            # Add more paths as needed
        ]
        if request.path not in excluded_paths and not request.path.startswith('/admin/'):
            token = request.META.get('HTTP_AUTHORIZATION', None)
            if not token or not token.startswith('Token '):
                return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)
            
            token_key = token.split(' ')[1]
            try:
                token = Token.objects.get(key=token_key)
                # request.user_id = token.user_id
                userprofile = UserProfile.objects.get(user_id = token.user_id)
                request.user_id = userprofile.id
            except Token.DoesNotExist:
                return JsonResponse({'detail': 'Invalid token.'}, status=401)
        
        response = self.get_response(request)
        return response
