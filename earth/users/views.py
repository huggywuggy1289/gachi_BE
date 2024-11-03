from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.shortcuts import redirect, render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import CustomReadOnly
from .serializers import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from .renderers import UserJSONRenderer
from .forms import *
# 토큰 발급받도록 뷰 변경
# 회원가입
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=request.data['username'])
        refresh = RefreshToken.for_user(user)
        response.data['token'] = str(refresh.access_token)
        return response

# 로그인 뷰
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data  # 토큰 받아오기
        return Response({"token": token.key}, status=status.HTTP_200_OK)

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
class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # 요청한 사용자의 객체를 가져옴

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()  # user 인스턴스 가져오기
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # PATCH 요청 처리
        serializer.is_valid(raise_exception=True)  # 유효성 검사
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

# 테마 변경