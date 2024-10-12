from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *

# 유저 테이블과 프로필 테이블이 한 모델인 것처럼 함께 관리할 수 있도록 admin에 등록
class ProfileInline(admin.StackedInline):
    # admin.StackedInline은 장고 어드민에서 User과 관련된 다른 모델(Profile 모델)
    # 을 한 페이지에서 보여주기 위한 클래스이다.
    model = Profile # 관련된 다른 모델 이름
    can_delete = False # 관리자가 해당 인라인에서 프로필을 삭제할 수 없도록 설정
    verbose_name_plural = "profile" # admin에서 해당 인라인의 이름을 표시할때 사용함.

class UserAdmin(BaseUserAdmin):
    # 이 클래스에 ProfileInline을 추가하여 User페이지에서 프로필 모델과 관련된 데이터를 함께 볼 수 있도록 추가
    inlines = (ProfileInline, )

admin.site.unregister(User) # 기본 유저 모델의 어드민을 비활성화(제거)
admin.site.register(User, UserAdmin) # 대신 직접설정한 클래스를 등록
admin.site.register(Profile)
# >> 이과정에서 ProfileInline이 포함된 새로운 사용자관리페이지 사용가능


