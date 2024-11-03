from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileView.as_view()),
    path('profile/update/', UpdateProfileView.as_view(), name='update-profile'),
    path('delete/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('contact/', ContactView.as_view(), name = 'contact'),
    path('order_detail/', OrderListView.as_view(), name = 'order_detail'),
]
