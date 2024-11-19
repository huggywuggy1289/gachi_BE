from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.http import FileResponse # 파일 다운로드
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import default_storage
from .models import *
from .serializers import *
from users.models import User

"""
광고와 아이템은 admin에서 등록하면 됨
아이템의 note 필드는 admin에서 등록하지 않고 빈칸으로 두면 됨
"""

# 아이템 리스트
class MarketAPIView(APIView):
    permission_class = [IsAuthenticated]

    def get(self, request):
        items = Item.objects.all()
        user = request.user

        item_serializer = ItemSerializer(items, many=True, context={'request': request})
        user_point_serializer = UserPointsSerializer(user)

        return Response({
            "item": item_serializer.data,
            "points": user_point_serializer.data
            }, status=status.HTTP_200_OK)

# 아이템 디테일
class ItemDetailAPIView(APIView):
    permission_class = [IsAuthenticated]

    def get(self, request, pk):
        items = get_object_or_404(Item, id=pk)
        item_serializer = ItemDetailSerializer(items, context={'request': request})

        user = request.user
        user_point_serializer = UserPointsSerializer(user)
        
        # 구매 여부 확인
        purchased = Purchase.objects.filter(user=user, item=items).exists()
        
        return Response({
            "item": item_serializer.data,
            "points": user_point_serializer.data,
            "button_text": "다운받기" if purchased else "구매하기"
        }, status=status.HTTP_200_OK)

    def post(self, request, pk):
        item = get_object_or_404(Item, id=pk)
        serializer = PurchaseSerializer(data=request.data, context={'request': request})

        user = request.user
        user_point = user.points  # 사용자의 포인트 확인
        item_price = item.price  # 아이템의 비용

        if user_point < item_price:
            # 포인트가 부족한 경우
            return Response({"message": "포인트가 부족합니다."}, status=status.HTTP_202_ACCEPTED)
        
        if serializer.is_valid():
            # 이미 구매한 경우
            if Purchase.objects.filter(user=user, item=item).exists():
                return Response({"message": "이미 구매한 아이템입니다."}, status=status.HTTP_202_ACCEPTED)
            
            serializer.save(item=item)  # 아이템을 시리얼라이저에 추가
            return Response({"message": "구매가 완료되었습니다."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 아이템 다운로드
class ItemDownloadView(APIView):
    def get(self, request, pk):
        try:
            item = Item.objects.get(pk=pk)
            file_name = item.item_image.name  # 파일 이름
            file_url = item.item_image.url  # S3의 URL

            # S3 URL에서 파일을 가져오기
            response = FileResponse(default_storage.open(file_name, 'rb'), as_attachment=True, filename=file_name)

            # 이미지의 확장자에 따라 Content-Type 설정
            if file_name.endswith('.png'):
                response['Content-Type'] = 'image/png'
            else:
                response['Content-Type'] = 'image/jpeg'

            return response
        except Item.DoesNotExist:
            return Response({"error": "아이템을 찾을 수 없습니다."}, status=202)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

"""
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
            return Response({"error": "아이템을 찾을 수 없습니다."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
"""