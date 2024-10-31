from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.http import FileResponse # 파일 다운로드

from .models import *
from .serializers import *

"""
할일
- 사용자 포인트 보여주기
- 포인트 차감 구현
- 시리얼라이저에서 구매 전이면 "구매" 버튼 / 구매 후면 "다운"버튼으로 보이도록 구현
>>>>> model에서 button 필드 추가해서 하면 될 듯?
"""

# 여긴 나중에 삭제
class ItemAPIView(APIView):
    def get(self, request):
        items = Item.objects.all()
        item_serializer = ItemSerializer(items, many=True)
        return Response(item_serializer.data, status=status.HTTP_200_OK)

class AdvertisementAPIView(APIView):
    def get(self, request):
        advertisements = Advertisement.objects.all()
        advertisement_serializer = AdvertisementSerializer(advertisements, many=True)
        return Response(advertisement_serializer.data, status=status.HTTP_200_OK)
#

#이거 아이템 사진 이름 가격만 나오도록 바꿔야 함
class MarketAPIView(APIView):
    def get(self, request):
        items = Item.objects.all()
        advertisements = Advertisement.objects.all()
        item_serializer = ItemSerializer(items, many=True, context={'request': request})
        advertisement_serializer = AdvertisementSerializer(advertisements, many=True, context={'request': request})

        return Response({
            "advertisement":advertisement_serializer.data,
            "item": item_serializer.data
            }, status=status.HTTP_200_OK)

# 아이템 디테일
class ItemDetailAPIView(APIView):
    def get(self, request, pk):
        items = get_object_or_404(Item, id=pk)
        item_serializer = ItemDetailSerializer(items, context={'request': request})
        return Response(item_serializer.data, status=status.HTTP_200_OK)

# 아이템 다운로드
class ItemDownloadView(APIView):
    def get(self, request, pk):
        try:
            item = Item.objects.get(pk=pk)
            file_path = item.item_image.path  # 이미지 파일의 경로
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=item.item_image.name)

            # 이미지의 확장자에 따라 Content-Type 설정
            if item.item_image.name.endswith('.png'):
                response['Content-Type'] = 'image/png'
            else:
                response['Content-Type'] = 'image/jpeg'

            return response
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)