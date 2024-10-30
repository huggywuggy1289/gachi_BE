from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('tutorial/', TutorialView.as_view(), name = 'tutorial'),
    path('card_post/', CardPostView.as_view(), name = 'card_post'),
    # path('frame_selection/', FrameSelection.as_view(), name = 'frame_selection'),
]

