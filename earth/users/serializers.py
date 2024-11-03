from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken
import logging

from market.models import Purchase
logger = logging.getLogger(__name__)
from rest_framework.authtoken.models import Token
from django.conf import settings
import jwt
from .models import *
from django.contrib.auth.password_validation import validate_password # 장고의 기본 패스워드 검증도구
from django.contrib.auth import authenticate # user 인증함수. 자격증명 유효한 경우 User객체 반환
from django.contrib.auth import get_user_model # userid로 로그인하기 위해
from rest_framework import serializers
from rest_framework.authtoken.models import Token # 토큰 모델
from rest_framework.validators import UniqueValidator # 이메일 중복방지를 위한 검증 도구
from django.core.validators import RegexValidator # 아이디 조건
from django.contrib.auth import get_user_model

# 회원가입 시리얼라이저
class RegisterSerializer(serializers.ModelSerializer):
    userid = serializers.CharField(
        help_text="아이디",
        required = True,
        max_length=150,
        validators = [
            UniqueValidator(queryset=User.objects.all()),   # id 중복검증
            RegexValidator(
                regex=r'^[\w.@+-]+$',  # 허용할 문자 및 숫자 정의
                message='150자 이하 문자, 숫자 그리고 @/./+/-/_만 가능합니다.',
                code='invalid_userid'
            ),
            ], 
    )
    password = serializers.CharField(
        help_text="비밀번호",
        write_only = True,
        required = True,
        validators = [validate_password] # import한 비밀번호에 대한 검증

    )
    password2 = serializers.CharField(
        help_text="비밀번호 재입력",
        write_only = True,
        required = True) # 검증은 한번만 해도 됨.

    class Meta:
        model = User
        fields = ('username', 'userid', 'password', 'password2')
        # username = 닉네임 / userid = 아이디
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
        )
        return data
    
    def create(self, validated_data):
        # create 요청을 통해 유저를 생성하고 토큰을 생성하게 함.
        user = User.objects.create_user(
            username=validated_data['username'],
            userid=validated_data['userid'],
        )

        user.set_password(validated_data['password'])
        user.save()
        # 각 유저 생성마다 토큰을 제작
        token = Token.objects.create(user=user)
        return user

# 로그인 시리얼라이저
class LoginSerializer(serializers.Serializer):
    userid = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        User = get_user_model()  # 현재 사용자 모델 가져오기
        try:
            # userid로 사용자 객체를 가져오기
            user = User.objects.get(userid=data['userid'])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"error": "Unable to log in with provided credentials."}
            )
        
        # 사용자 객체가 존재하면 authenticate 사용
        if user.check_password(data['password']):
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials."}
        )
    
# 모델 시리얼라이저
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ()

# 회원정보 수정 시리얼라이저
class UpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def update(self, instance, validated_data):
        # 비밀번호 업데이트
        password = validated_data.pop('password')
        instance.username = validated_data.get('username', instance.username)
        instance.set_password(password)  # 비밀번호 해시화
        instance.save()
        return instance

# 구매내역 시리얼라이저
class OrderListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Purchase
        fields = ['item']