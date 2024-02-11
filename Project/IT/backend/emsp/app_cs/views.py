from datetime import datetime

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import fromstr
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import ChargingStation, ChargingSocket
from .serializers import ChargingStationModelSerializer, ChargingStationModelDetailSerializer, \
    ChargingStationExternalStatus, ChargingStationInternalStatus, ChargingSocketModelSerializer


def get_available_sockets(start_time, end_time):
    available_sockets = ChargingSocket.objects.filter(
        Q(sockets__start_time__gt=end_time) | Q(sockets__end_time__lt=start_time)
    ).distinct()
    return available_sockets


class ChargingStationModelViewSet(ModelViewSet):
    queryset = ChargingStation.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = ChargingStationModelSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    filterset_fields = [
        'power_source',
        'stations__type'
    ]

    ordering_fields = [
        'location',
        'price',
        'discount',
        'stations__type'
    ]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return super().get_permissions()

        else:
            return [IsAdminUser(), ]

    def filter_queryset(self, queryset):
        ordering = self.request.query_params.get('ordering')
        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')

        if start_time and end_time:
            try:
                start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
                end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M')
            except ValueError:
                pass
            else:
                if start_time < end_time:
                    queryset = queryset.filter(
                        stations__in=get_available_sockets(start_time, end_time)
                    )

        if ordering in ['location', '-location']:
            latitude = self.request.query_params.get('latitude')
            longitude = self.request.query_params.get('longitude')

            if not latitude or not longitude:
                return super().filter_queryset(queryset)

            user_location = fromstr(f'POINT({longitude} {latitude})', srid=4326)

            order_by = 'distance'

            if ordering == '-location':
                order_by = f'-{order_by}'

            return queryset.annotate(distance=Distance('location', user_location)).order_by(order_by)

        return super().filter_queryset(queryset)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ChargingStationModelDetailSerializer
        return super().get_serializer_class()

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def external_status(self, request, pk, *args, **kwargs):

        instance = get_object_or_404(ChargingStation, pk=pk)

        return Response(ChargingStationExternalStatus(instance).data)

    @action(detail=True, methods=['get'])
    def internal_status(self, request, pk, *args, **kwargs):

        instance = get_object_or_404(ChargingStation, pk=pk)

        return Response(ChargingStationInternalStatus(instance).data)

    @action(detail=True, methods=['patch'])
    def set_power_source(self, request, pk, *args, **kwargs):

        instance = get_object_or_404(ChargingStation, pk=pk)

        power_source = request.data.get('power_source')
        source_id = request.data.get('source_id')
        price = request.data.get('source_price')

        if power_source == 'DSO':

            try:
                price = int(price)
            except:  # noqa
                price = None
            instance.set_dso(source_id, price)

        elif power_source == 'Battery':
            instance.set_battery()

        elif power_source == 'Mix':
            instance.set_mix(source_id)

        return Response({'message': f'Power source set to {instance.power_source} with id:{source_id} successfully'})


class ChargingSocketModelViewSet(ModelViewSet):
    queryset = ChargingSocket.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = ChargingSocketModelSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return super().get_permissions()

        else:
            return [IsAdminUser(), ]
