from django.db import models
from accounts.models import UserProfile
from django.contrib.auth.models import User 
from django.db.models.signals import post_save,post_delete
from django.contrib.auth.models import User 
from django.dispatch import receiver



class Post(models.Model):
    user = models.ForeignKey(UserProfile , on_delete=models.CASCADE)

    post_data = models.JSONField(default=dict) # Store post related data in json format
    reaction_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return "{}--{}".format(self.user.name , self.id)
    

class PostReaction(models.Model):
    REACTION_TYPE = {
        'like':'like',
        'dislike':'dislike',
        'appriciate':'appriciate',
        'funny':'funny'
    }
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile , on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=20 )

    def __str__(self):
        return "{}-{}".format(self.post.id , self.user.id)

    class Meta:
        unique_together = ['post_id', 'user_id']

class PostComment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    post_comment = models.TextField()

    def __str__(self):
        return "{} - {}",format(self.post.id , self.post_comment)


class Connection(models.Model):
    '''
    Maintaining a 1-1 relationships. 
    If A -> B:
    then B-> A (create another instance). 

    if A !-> B:
    then B!-> A (delete another instance).

    Create Two signals. One for PostSave and One for PostDelete
    '''
    user_from = models.ForeignKey(UserProfile, related_name='connections_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey(UserProfile, related_name='connections_to', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # OVerride this for follow back time

    def __str__(self):
        return "{}-{}".format(self.user_from, self.user_to)
    
    class Meta:
        unique_together = ['user_from', 'user_to']

# @receiver(post_save, sender=Connection) 
# def create_profile(sender, instance, created, **kwargs):
# 	if created:
# 		Connection.objects.create(user_from = instance.user_to , user_to = instance.user_from)

# Can't handle this here. Handle this in views        
# @receiver(post_delete, sender=Connection)
# def delete_reciprocal_connection(sender, instance, **kwargs):
#     try:
#         reciprocal_connection = Connection.objects.get(user_from=instance.user_to, user_to=instance.user_from)
#         reciprocal_connection.delete()
#     except Connection.DoesNotExist as E:
#         raise Exception(str(E))
