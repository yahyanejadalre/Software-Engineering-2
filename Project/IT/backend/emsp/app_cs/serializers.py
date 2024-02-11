from datetime import timedelta

from django.utils.timezone import now
from rest_framework import serializers

from .models import ChargingStation, ChargingSocket


class ChargingStationModelSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField(read_only=True)

    geo_point = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ChargingStation
        fields = [
            'id',
            'location',
            'geo_point',
            'power_source',
            'price',
        ]

    @staticmethod
    def get_geo_point(obj):
        return {
            'x': obj.location.x,
            'y': obj.location.y,
        }

    @staticmethod
    def get_location(obj: ChargingStation):
        """
        return google map link
        :param obj:
        :return:
        """
        return f'https://www.google.com/maps/search/?api=1&query={obj.location.y},{obj.location.x}'


class ChargingSocketModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingSocket
        fields = '__all__'

    def update(self, instance, validated_data):
        is_charging = validated_data.pop('is_charging', None)

        if is_charging is True:
            instance.start_charging()
        elif is_charging is False:
            instance.stop_charging()

        return super().update(instance, validated_data)


class ChargingSocketStatusSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()
    next_available_time = serializers.SerializerMethodField()

    class Meta:
        model = ChargingSocket
        fields = [
            'is_available',
            'is_charging',
            'current_vehicle_charging_level',
            'next_available_time',
            'type',
            'identifier',
        ]

    @staticmethod
    def get_is_available(obj: ChargingSocket):
        _now = now()
        return obj.is_available(_now, _now + timedelta(minutes=1))

    @staticmethod
    def get_next_available_time(obj: ChargingSocket):
        from app_booking.models import BookingHistory

        _now = now()

        next_available_time = BookingHistory.objects.filter(
            charging_socket=obj,
            end_time__lt=_now
        ).latest('end_time')
        return next_available_time.start_time


class ChargingStationModelDetailSerializer(ChargingStationModelSerializer):
    charging_sockets = serializers.SerializerMethodField()

    class Meta(ChargingStationModelSerializer.Meta):
        fields = ChargingStationModelSerializer.Meta.fields + ['charging_sockets', ]

    @staticmethod
    def get_charging_sockets(obj: ChargingStation):
        return ChargingSocketModelSerializer(obj.stations, many=True).data


class ChargingStationExternalStatus(serializers.ModelSerializer):
    sockets = serializers.SerializerMethodField()

    location = serializers.SerializerMethodField(read_only=True)

    geo_point = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ChargingStation
        fields = [
            'id',
            'sockets',
            'location',
            'geo_point',
            'power_source',
            'price',
            'source_id',
        ]

    @staticmethod
    def get_geo_point(obj):
        return {
            'x': obj.location.x,
            'y': obj.location.y,
        }

    @staticmethod
    def get_location(obj: ChargingStation):
        """
        return google map link
        :param obj:
        :return:
        """
        return f'https://www.google.com/maps/search/?api=1&query={obj.location.y},{obj.location.x}'

    @staticmethod
    def get_sockets(obj: ChargingStation):
        return ChargingSocketStatusSerializer(ChargingSocket.objects.filter(station=obj), many=True).data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ChargingStationInternalStatus(serializers.ModelSerializer):
    sockets = serializers.SerializerMethodField()

    location = serializers.SerializerMethodField(read_only=True)

    geo_point = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ChargingStation
        fields = [
            'id',
            'sockets',
            'vehicle_charged',
            'battery_level',
            'power_source',
            'price',
            'source_id',
            'location',
            'geo_point',
        ]

    @staticmethod
    def get_geo_point(obj):
        return {
            'x': obj.location.x,
            'y': obj.location.y,
        }

    @staticmethod
    def get_location(obj: ChargingStation):
        """
        return google map link
        :param obj:
        :return:
        """
        return f'https://www.google.com/maps/search/?api=1&query={obj.location.y},{obj.location.x}'

    @staticmethod
    def get_sockets(obj: ChargingStation):
        return ChargingSocketStatusSerializer(ChargingSocket.objects.filter(station=obj), many=True).data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
