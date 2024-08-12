from django.urls import path 
from .views import * 

urlpatterns =[
    path('register', Auth.as_view({'post':'register'})),
    path('login', Auth.as_view({"post":'login'})),
    path('logout', Auth.as_view({'post':'logout'})),
    path('users', UserView.as_view({'get':'get_users'}))
]