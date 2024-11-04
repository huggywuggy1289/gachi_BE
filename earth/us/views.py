from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from users.models import User,UserTheme

class UsAPIView(APIView):
    permission_class = [IsAuthenticated]

    def get(self, request):
        # 현재 로그인한 사용자 인스턴스 가져오기
        us_instance = get_object_or_404(Us, user=request.user)

        # 레벨 하락 확인
        level_downgraded = us_instance.check_level_downgrade()

        serializer = UsSerializer(us_instance)

        # 전체 사용자 순위 계산
        all_users = Us.objects.order_by('-level', '-step', 'user_id')

        # 순위 매기기
        user_rank = 0
        for idx, user in enumerate(all_users):
            if user.user == request.user:
                user_rank = idx + 1  # 인덱스는 0부터 시작하므로 +1
                break

        # 상위 3등 사용자 가져오기
        top_users = all_users[:3]
        top_users_data = UsSerializer(top_users, many=True).data

        # 현재 테마
        user_theme, created = UserTheme.objects.get_or_create(user=request.user)

        return Response({
            "current_theme": user_theme.selected_theme,
            "my": serializer.data,
            "my_rank": user_rank,
            "level_downgrade": level_downgraded,
            "top_users": top_users_data
        }, status=status.HTTP_200_OK)