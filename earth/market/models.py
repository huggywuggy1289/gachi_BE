from django.db import models
from users.models import User

class Market(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# 구매 아이템
class Item(models.Model):
    # ('db저장값', '사용자에게보이는값')
    ITEM_TYPE_CHOICES = [
        ('sticker', '스티커'),
        ('theme', '테마'),
        ('frame', '프레임'),
    ]

    item_name = models.CharField(max_length=50)         # 아이템 이름
    description = models.TextField(max_length=100)      # 아이템 설명
    price = models.IntegerField()                       # 아이템 가격
    item_image = models.ImageField(upload_to='items/')  # 아이템 이미지
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)  # 아이템 타입
    note = models.TextField(max_length=200, blank=True)             # 참고 사항

    def __str__(self):
        return self.item_name

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')  # 사용자와 품목의 조합은 유일해야 함

    def __str__(self):
        return f"{self.user.username} purchased {self.item.item_name}"