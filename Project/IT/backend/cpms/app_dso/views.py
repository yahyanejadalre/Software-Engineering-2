import random

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import DSO
from .serializers import DSOModelSerializer


class DSOModelViewSet(ModelViewSet):
    queryset = DSO.objects.all()
    serializer_class = DSOModelSerializer
    permission_classes = [IsAdminUser, ]
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    filterset_fields = [
        'is_available',
        'active',
    ]

    ordering_fields = [
        'price',
        'is_available',
        'updated_at',
    ]

    @action(detail=False, methods=['post'])
    def update_dso_status(self, request, *args, **kwargs):
        """
        randomly change DSOs fields in database using bulk_update
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        updated_list = []
        for dso in DSO.objects.all():
            dso.price = random.randint(10, 20)
            dso.is_available = random.choice([True, False])

            if not dso.is_available:
                dso.active = False

            updated_list.append(dso)

        DSO.objects.bulk_update(updated_list, ['price', 'is_available', 'active'], batch_size=1000)

        return Response({'message': f'{len(updated_list)} DSOs were updated'})

    @transaction.atomic
    @action(detail=True, methods=['patch'])
    def activate(self, request, pk, *args, **kwargs):
        DSO.objects.filter(is_available=True).filter(pk=pk).select_for_update().update(active=True)
        DSO.objects.exclude(pk=pk).select_for_update().update(active=False)

        return Response({'message': f'DSO with id={pk} was activated'})
