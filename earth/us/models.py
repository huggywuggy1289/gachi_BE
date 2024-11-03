from django.db import models
from users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Us(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    step = models.IntegerField(default=0)

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return self.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Us.objects.create(user=instance)