from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# 활용할 필드목록
# useranme: ID로 활용, required=True
# email: required=True
# password: required=True

# user확장
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=40, blank=True)
    image = models.ImageField(upload_to='profile/', default='default.png')

# User가 생성될 때 자동으로 프로필 생성
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

