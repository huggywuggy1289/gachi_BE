# 배포할때 추가할 코드 있음
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok"}, status=200)