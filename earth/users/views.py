from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer # 회원가입 시리얼라이저의 클래스명
from .models import *
from django.views.decorators.csrf import csrf_exempt
import logging

# view is mostly simple because serializer code.
# 회원가입
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all() # 기본적으로 유저 쿼리셋 가져오고
    serializer_class = RegisterSerializer # 시리얼라이저 등록하는 형식이 views의 기본이 된다.

# 로그인
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data # 토큰 받아오기
        return Response({"token" : token.key}, status=status.HTTP_200_OK)
    
# 프로필 모델(가져오는 기능, 수정하는 기능 요구>> RetrieveUpdateAPIView)
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'pk' # *

# 닉네임 중복 방지(함수형으로)
# 오류해결 : https://stackoverflow.com/questions/5895588/django-multivaluedictkeyerror-error-how-do-i-deal-with-it
@csrf_exempt
def check_nickname(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')  # form-data에서 닉네임 가져오기
        if Profile.objects.filter(nickname=nickname).exists():  # 중복 체크
            return JsonResponse({'status': 'fail', 'message': '중복되는 이름입니다.'}, status=400)
        else:
            return JsonResponse({'status': 'success', 'message': '사용가능한 이름입니다.'})
    return JsonResponse({'error': 'Invalid request'}, status=400)