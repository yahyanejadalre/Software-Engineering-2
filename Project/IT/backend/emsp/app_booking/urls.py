from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookingModelViewSet

router = DefaultRouter()

router.register(r'', BookingModelViewSet, basename='bookings')

urlpatterns = [
    path('', include(router.urls)),
]
