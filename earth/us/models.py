from django.db import models
from users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

class Us(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    step = models.IntegerField(default=0)
    last_level_downgrade = models.DateTimeField(null=True, blank=True)  # 마지막 레벨 하락 시간

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return self.username

    def check_level_downgrade(self):
        if self.level == 0:
            return False  # 레벨이 0이면 하락하지 않음

        if self.last_level_downgrade is None:
            self.last_level_downgrade = timezone.now()
            self.save()
            return False  # 처음 하락이므로 하락하지 않음

        time_since_last_downgrade = timezone.now() - self.last_level_downgrade

        # 기준 시간을 5분으로 설정 (테스트용) minutes=5
        if time_since_last_downgrade >= timedelta(days=7):
            # 레벨 하락
            new_level = max(0, int(self.level * 0.5))  # 레벨이 0 미만으로 떨어지지 않도록
            self.level = new_level
            self.last_level_downgrade = timezone.now()  # 현재 시간 저장
            self.save()
            return True  # 레벨이 하락했음을 반환
        return False  # 레벨이 하락하지 않았음을 반환


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Us.objects.create(user=instance)