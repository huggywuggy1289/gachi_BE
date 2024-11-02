import base64
from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError

# https://tyoon9781.tistory.com/entry/django-rest-framework-1-serialization

# 튜토리얼 시리얼라이저
class TutorialSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    tutorial_completed = serializers.BooleanField(required = False)

    class Meta:
        model = UserProfile
        fields = ['id', 'tutorial_completed']

# 카드 작성 시리얼라이저(모든 것이 작성 잘 되었는지 검토 필요)
class CardPostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CardPost
        fields = ["image", "explanation", "keyword"]

    def validate(self, data):
        if not data.get("image"):
            raise serializers.ValidationError({"image": "이미지를 업로드해야 합니다."})
        if not data.get("explanation"):
            raise serializers.ValidationError({"explanation": "사진 설명을 입력해야 합니다."})
        if not data.get("keyword"):
            raise serializers.ValidationError({"keyword": "키워드를 선택해야 합니다."})
        
        else:
            return data
        
# 프레임 시리얼라이저
class FrameSerializer(serializers.ModelSerializer):
    frame_completed = serializers.BooleanField(required = False)

    class Meta:
        model = Frame
        fields = ['user', 'frame_completed']
        extra_kwargs = {'user': {'read_only': True}}  # user 필드는 자동으로 설정

# 이미지 저장 시리얼라이저
class PhotoSerializer(serializers.ModelSerializer):
    decorated_image = serializers.ImageField(use_url = True)

    def validate_decorated_image(self, value):
        if not value:
            raise serializers.ValidationError("Decorated image is required.")
        return value

    class Meta:
        model = Photo
        fields = ('decorated_image', 'card_post')

# 이미지 공유 > 포인트 적립
class ImageShareSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ImageShare
        fields = ('card_post', 'point')