from django.urls import path
from .views import *

urlpatterns = [
    path('us/', UsAPIView.as_view()),
]
