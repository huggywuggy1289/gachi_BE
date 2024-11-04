from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

# 활용할 필드목록
# useranme: ID로 활용, required=True
# email: required=True
# password: required=True

class User(AbstractUser):
    userid = models.CharField(max_length=150, unique=True)
    points = models.IntegerField(default=0)  # 사용자 포인트 필드 추가
    order_detail = models.ForeignKey(
        'market.Purchase',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='orders'
    )  # 구매내역 조회 필드 추가

    @property
    def token(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)

# User 확장
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

# User가 생성될 때 자동으로 프로필 생성
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        #UserTheme.objects.create(user=instance)

# 테마
class UserTheme(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    selected_theme = models.CharField(max_length=50, default='기본 테마')

    def __str__(self):
        return f"{self.user.username}'s Theme"