from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('tutorial/', TutorialView.as_view(), name = 'tutorial'),
]

