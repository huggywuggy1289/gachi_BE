from django.urls import path
from .views import ProfileView, RegisterView, LoginView
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/<int:pk>/', ProfileView.as_view()),
    path('check-nickname/', views.check_nickname, name='check_nickname'),  # 중복확인 뷰 추가
]
