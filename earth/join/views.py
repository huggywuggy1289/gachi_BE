from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import TutorialSerializer
from .models import *
from rest_framework import status

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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)