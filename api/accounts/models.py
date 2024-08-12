from django.db import models
from django.contrib.auth.models import User 
from django.shortcuts import redirect


class UserProfile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True , blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.user.username
    


from django.db.models.signals import post_save 
from django.contrib.auth.models import User 
from django.dispatch import receiver


@receiver(post_save, sender=User) 
def create_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)