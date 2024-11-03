from rest_framework import serializers
from .models import *
from market.serializers import UserPointsSerializer
from join.models import CardPost

class UsSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    points = serializers.IntegerField(source='user.points', read_only=True)
    total_cards = serializers.SerializerMethodField() # 총 누적된 카드 개수

    class Meta:
        model = Us
        fields = ("user", "username", "level", "step", "points", "total_cards")

    def get_total_cards(self, obj):
        return CardPost.objects.filter(author=obj.user).count()