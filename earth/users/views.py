from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.shortcuts import redirect, render
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import CustomReadOnly
from .serializers import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from .renderers import UserJSONRenderer
from .forms import *
from market.models import Item, Purchase
from rest_framework_simplejwt.tokens import RefreshToken

# 토큰 발급받도록 뷰 변경
# 회원가입
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        # 유효성 검사
        if serializer.is_valid():
            # 사용자 생성
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "userid": user.userid,
                "username": user.username,
                "token": str(refresh.access_token),
                "message": "회원가입이 완료되었습니다."
            }, status=status.HTTP_201_CREATED)

        # 유효성 검사 실패 시 200 응답으로 오류 메시지 반환
        return Response({
            "errors": serializer.errors,
            "message": "회원가입에 실패했습니다."
        }, status=status.HTTP_200_OK)

# 로그인 뷰
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        # 유효성 검사
        if not serializer.is_valid():
            return Response({
                "errors": serializer.errors,
                "message": "로그인에 실패했습니다."
            }, status=status.HTTP_200_OK)

        token = serializer.validated_data['token']  # 토큰 받아오기
        user = serializer.validated_data['user']  # 사용자 정보 가져오기
        return Response({
            "token": token.key,
            "last_login": user.last_login
        }, status=status.HTTP_200_OK)

# 로그아웃 뷰(post)
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 요청한 사용자의 토큰을 가져옵니다.
        token = request.auth
        # 사용자의 토큰 삭제
        if token:
            token.delete()
        return Response({"message": "Successfully logged out."}, status=200)

# 프로필 모델
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

# 회원정보 수정 뷰
class UpdateProfileView(generics.RetrieveAPIView):
    serializer_class = UpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # 요청한 사용자의 객체를 가져옴

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()  # user 인스턴스 가져오기
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # PATCH 요청 처리
        
        # 유효성 검사
        if not serializer.is_valid():
            return Response({
                "errors": serializer.errors,
                "message": "프로필 업데이트에 실패했습니다."
            }, status=status.HTTP_200_OK)

        serializer.save()  # 데이터 저장
        return Response({"username": serializer.data['username']})  # 업데이트된 닉네임 반환

# 회원탈퇴
class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def delete(self, request, *args, **kwargs):
        # 현재 요청한 사용자의 정보를 가져옵니다.
        user = request.user
        user.delete()  # 사용자를 삭제합니다.
        return Response({"detail": "User has been deleted."}, status=status.HTTP_204_NO_CONTENT)

# 문의하기
class ContactView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"문의는 이곳으로 해주세요! : Instagram @joinusearth_24"})

# 구매목록조회
class OrderListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        # 현재 로그인한 사용자의 구매 내역을 반환
        return Purchase.objects.filter(user=self.request.user)


# 테마 조회, 변경
class UserThemeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_theme, created = UserTheme.objects.get_or_create(user=request.user)
        
        # 사용자가 구매한 테마 목록 조회
        purchased_items = Purchase.objects.filter(user=request.user)
        purchased_themes = [purchase.item.item_name for purchase in purchased_items if purchase.item.item_type == 'theme']

        themes = [{"theme_name": "기본 테마", "is_selected": user_theme.selected_theme == "기본 테마"}]
        
        # 구매한 테마가 있을 경우 추가
        for theme_name in purchased_themes:
            themes.append({"theme_name": theme_name, "is_selected": user_theme.selected_theme == theme_name})

        return Response(themes, status=status.HTTP_200_OK)

    def post(self, request):
        user_theme, created = UserTheme.objects.get_or_create(user=request.user)
        selected_theme = request.data.get("selected_theme")

        purchased_items = Purchase.objects.filter(user=request.user)
        purchased_themes = [purchase.item.item_name for purchase in purchased_items if purchase.item.item_type == 'theme']

        # 선택된 테마 업데이트
        if (selected_theme in purchased_themes) or (selected_theme == "기본 테마"):
            user_theme.selected_theme = selected_theme
            user_theme.save()

            return Response({"message": "테마가 변경되었습니다."}, status=status.HTTP_200_OK)
        
        return Response({"message": "테마를 구매 후 변경해주세요."}, status=status.HTTP_202_ACCEPTED)