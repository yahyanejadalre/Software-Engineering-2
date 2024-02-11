from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ChargingStationModelViewSet, ChargingSocketModelViewSet

router = DefaultRouter()
router.register('', basename='charging station', viewset=ChargingStationModelViewSet)
router.register('socket', basename='charging sockets', viewset=ChargingSocketModelViewSet)

urlpatterns = [
    path('', include(router.urls))
]
