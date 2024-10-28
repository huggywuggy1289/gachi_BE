from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
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
    
# 프로필 모델
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

#회원정보 수정 뷰
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




# 닉네임 중복 방지(함수형으로)
# 오류해결 : https://stackoverflow.com/questions/5895588/django-multivaluedictkeyerror-error-how-do-i-deal-with-it
# @csrf_exempt
# def check_nickname(request):
#     if request.method == 'POST':
#         nickname = request.POST.get('nickname')  # form-data에서 닉네임 가져오기
#         if Profile.objects.filter(nickname=nickname).exists():  # 중복 체크
#             return JsonResponse({'status': 'fail', 'message': '중복되는 이름입니다.'}, status=400)
#         else:
#             return JsonResponse({'status': 'success', 'message': '사용가능한 이름입니다.'})
#     return JsonResponse({'error': 'Invalid request'}, status=400)