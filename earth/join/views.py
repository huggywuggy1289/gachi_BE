from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from rest_framework import status
from django.shortcuts import redirect

class TutorialView(APIView):
    permission_class = [IsAuthenticated]

    # 유저의 튜토리얼 상태 확인 (0인지 1인지)
    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user = request.user)
        serializer = TutorialSerializer(profile)
        return Response(serializer.data)
    
    # 튜토리얼을 완료했음을 알리는 요청
    def post(self, request):
        profile, created = UserProfile.objects.get_or_create(user = request.user)
        serializer = TutorialSerializer(profile, data=request.data, partial=True) # data전달 필요, 인스턴스 자체를 전달하면 안됨.
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 카드작성뷰, 튜토리얼 완료못한 사람은 무조건 튜토리얼 끝낸 후 작성가능
class CardPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 사용자 프로필에서 튜토리얼 완료 여부 확인
        profile, created =  UserProfile.objects.get_or_create(user = request.user)

        if not profile.tutorial_completed:
            return Response({"message": "튜토리얼을 완료해야 카드 작성이 가능합니다."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CardPostSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({
                "message": "카드가 성공적으로 작성되었습니다.",
                "redirect_url": "/join/frame_selection/"
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
