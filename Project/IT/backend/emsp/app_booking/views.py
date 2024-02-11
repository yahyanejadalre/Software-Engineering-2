from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import BookingHistory
from .serializers import BookingChargingSocketSerializer, BookingHistorySerializer


class BookingModelViewSet(ModelViewSet):
    queryset = BookingHistory.objects.all()
    serializer_class = BookingHistorySerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    filterset_fields = [
        'status',
        'charging_socket'
    ]

    ordering_fields = [
        'start_time',
        'end_time',
        'price',
        'status',
        'created_at'
    ]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingChargingSocketSerializer
        return super().get_serializer_class()
