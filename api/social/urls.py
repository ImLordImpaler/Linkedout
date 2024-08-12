from django.urls import path 
from .views import * 


urlpatterns = [
    # Post Apis
    path('posts', PostView.as_view({'get':'show_posts', 'post':'create_post'})),
    path('post/<str:pk>', PostView.as_view({'get':'get_post', 'delete':'delete_post'})),
    
    #Interaction

    path('post_reaction', Interaction.as_view({'post':'create_reaction'})),
    path('post_comment', Interaction.as_view({'post':'create_comment'})),
    path('comment/<str:pk>', Interaction.as_view({'get':'get_comment', 'delete':'delete_comment'})),
    path('connection', Interaction.as_view({'post':'create_connection', 'delete':'delete_connection'})),
    path('connections', Interaction.as_view({'get':'get_connections'})),


]