from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', JoinView.as_view(), name = 'join'),
    path('list/', PostListAPIView.as_view(), name='list_monthly'),  # 월별 카드 보기 join/list/?monthly=int/
    path('tutorial/', TutorialView.as_view(), name = 'tutorial'),
    path('card_post/', CardPostView.as_view(), name = 'card_post'),
    path('frame_selection/', FrameSelection.as_view(), name = 'frame_selection'),
    path('completed/', CompletedView.as_view(), name = 'completed'),
    path('completed/<int:image_id>/', ImageShareView.as_view(), name='completed'),  # ImageShareView 추가
    #+
    path('imagedownload/<int:pk>/', ImageDownloadView.as_view(), name='download'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

