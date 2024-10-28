from django.urls import path
from .views import *

app_name = 'earthApp'

urlpatterns = [
    #삭제
    path('test_item/', ItemAPIView.as_view()),
    path('test_advertisement/', AdvertisementAPIView.as_view()),
    #

    path('market/', MarketAPIView.as_view()),
    path('item/<int:pk>/', ItemDetailAPIView.as_view()),
    path('item/download/<int:pk>/', ItemDownloadView.as_view()),
]
