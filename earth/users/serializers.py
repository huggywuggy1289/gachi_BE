from .models import *
from django.contrib.auth.password_validation import validate_password # 장고의 기본 패스워드 검증도구
from django.contrib.auth import authenticate # user 인증함수. 자격증명 유효한 경우 User객체 반환

from rest_framework import serializers
from rest_framework.authtoken.models import Token # 토큰 모델
from rest_framework.validators import UniqueValidator # 이메일 중복방지를 위한 검증 도구
from django.core.validators import RegexValidator # 아이디 조건

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
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user) # 토큰에서 유저필드를 찾은 후 반환
            # 딕셔너리로 전달되면 오류가 발생한다.
            return token
        # 아닐 경우
        raise serializers.ValidationError(
            {"error" : "Unable to log in with provided credentials."}
        )
    
# 모델 시리얼라이저
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ()