from django.urls import path
from .views import *

urlpatterns = [
    path('market/', MarketAPIView.as_view()),
    path('item/<int:pk>/', ItemDetailAPIView.as_view()),
    path('item/download/<int:pk>/', ItemDownloadView.as_view()),
]