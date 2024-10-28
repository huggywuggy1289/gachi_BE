from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/<int:pk>/', ProfileView.as_view()),
    path('current/', UserRetrieveUpdateAPIView.as_view()),
    path('delete/', UserDeleteAPIView.as_view(), name='user-delete'),
]
