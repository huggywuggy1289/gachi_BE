from rest_framework import serializers
from .models import *

# https://tyoon9781.tistory.com/entry/django-rest-framework-1-serialization

# 튜토리얼 시리얼라이저
class TutorialSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    tutorial_completed = serializers.BooleanField(required = False)

    class Meta:
        model = UserProfile
        fields = ['id', 'tutorial_completed']
