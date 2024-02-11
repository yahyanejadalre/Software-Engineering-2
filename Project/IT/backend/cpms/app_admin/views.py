from django.conf import settings
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from utilities.service import send_authenticated_request
from app_dso.models import DSO

EMSP_API_URL = settings.EMSP_API_URL

CS_API_URL = EMSP_API_URL + 'cs/'


class CSViewSet(ReadOnlyModelViewSet):
    queryset = None
    permission_classes = [IsAdminUser, ]
    serializer_class = None

    def list(self, request, *args, **kwargs):
        query_parameters = request.query_params.dict()
        new_url = CS_API_URL + '?' + '&'.join([f'{key}={value}' for key, value in query_parameters.items()])
        response = send_authenticated_request('get', new_url)

        return Response(response.json())

    def retrieve(self, request, *args, **kwargs):
        new_url = CS_API_URL + f'{kwargs["pk"]}/external_status'
        response = send_authenticated_request('get', new_url)
        return Response(response.json())

    @action(detail=True, methods=['get'])
    def internal_status(self, request, pk, *args, **kwargs):
        new_url = CS_API_URL + f'{pk}/internal_status'
        response = send_authenticated_request('get', new_url)
        return Response(response.json())

    @action(detail=True, methods=['get'])
    def external_status(self, request, pk, *args, **kwargs):
        new_url = CS_API_URL + f'{pk}/external_status'
        response = send_authenticated_request('get', new_url)
        return Response(response.json())

    @action(detail=True, methods=['patch'])
    def set_power_source(self, request, pk, *args, **kwargs):
        new_url = CS_API_URL + f'{pk}/set_power_source/'

        data = request.data

        if source_id := data.get('source_id'):
            if dso := DSO.objects.filter(identifire=source_id).first():
                price = dso.price

                data: dict = request.data.dict()
                data.update({'source_price': price})

        response = send_authenticated_request('patch', new_url, data=data)
        return Response(response.json())


class SocketChargingAPIView(APIView):
    permission_classes = [IsAdminUser, ]

    @staticmethod
    def patch(request, pk):
        new_url = CS_API_URL + f'socket/{pk}/'
        print(request.data)
        response = send_authenticated_request('patch', new_url, data=request.data)
        return Response(response.json())
