from rest_framework import serializers
from .models import *
from urllib.parse import urljoin

# 아이템 리스트
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            "item_name",
            "price",
            "item_image",
            "id",
            )

    def get_item_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.item_image.url)

# 아이템 디테일
class ItemDetailSerializer(serializers.ModelSerializer):
    note = serializers.SerializerMethodField()  # 동적 note 필드

    class Meta:
        model = Item
        fields = (
            "item_name",
            "description",
            "price",
            "item_image",
            "item_type",
            "note"
            )

    def get_item_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.item_image.url)

    # note 값을 동적으로 설정
    def get_note(self, obj):
        if obj.item_type == "sticker":
            return "*다운받아 사용해주세요!"
        elif obj.item_type == "theme":
            return "*마이>어스테마 바꾸기에서 테마 변경 가능합니다."
        else:  # "frame"
            return "*자동으로 프레임이 추가됩니다."

# 광고 배너
class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ("ad_title", "ad_image", "ad_link")

    def get_ad_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.item_image.url)