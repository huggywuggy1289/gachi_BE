from rest_framework import serializers
from .models import *
from urllib.parse import urljoin
from users.models import User

# 사용자 포인트
class UserPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "points")

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

# 아이템 구매
class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['item']

    def create(self, validated_data):
        user = self.context['request'].user
        item = validated_data['item']

        # 이미 구매한 품목인지 확인
        if Purchase.objects.filter(user=user, item=item).exists():
            raise serializers.ValidationError("이 품목은 이미 구매하였습니다.")
        
        # 사용자의 포인트 확인
        if user.points < item.price:
            raise serializers.ValidationError("포인트가 부족해서 상품을 구매할 수 없습니다.")

        # 포인트 차감
        user.points -= item.price
        user.save()

        purchase = Purchase.objects.create(user=user, **validated_data)
        return purchase
