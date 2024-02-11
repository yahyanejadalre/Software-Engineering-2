from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CSViewSet, SocketChargingAPIView

router = DefaultRouter()
router.register('cs', basename='charging stations', viewset=CSViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('socket/<pk>/', SocketChargingAPIView.as_view())
]
