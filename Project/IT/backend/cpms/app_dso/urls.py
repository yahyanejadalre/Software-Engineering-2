from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DSOModelViewSet

router = DefaultRouter()
router.register('', basename='dso', viewset=DSOModelViewSet)

urlpatterns = [
    path('', include(router.urls))
]
