from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

class CustomReadOnly(permissions.BasePermission):
# GET(조회)요청은 누구나, PUT/PATCH(수정 및 삭제 등)은 해당유저만
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # 데이터에 영향을 미치지않는 메소드라면 true로 반환시킨다.
            return True
        # 객체에 대한 작업을 요청한 사용자가 객체의 소유자일 경우에만 허용
        return obj.user == request.user