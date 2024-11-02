from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('list/', PostListAPIView.as_view(), name = 'list'),
    path('tutorial/', TutorialView.as_view(), name = 'tutorial'),
    path('card_post/', CardPostView.as_view(), name = 'card_post'),
    path('frame_selection/', FrameSelection.as_view(), name = 'frame_selection'),
    path('completed/', CompletedView.as_view(), name = 'completed'),
    path('image_share/<int:image_id>/', ImageShareView.as_view(), name='image_share'),  # ImageShareView 추가
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

