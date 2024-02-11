from django.db import transaction
from django.utils.timezone import now
from rest_framework import serializers

from app_booking.models import BookingHistory
from app_cs.models import ChargingSocket


class BookingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingHistory
        fields = '__all__'


class BookingChargingSocketSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()

    charging_socket = serializers.PrimaryKeyRelatedField(queryset=ChargingSocket.objects.all())

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs['start_time'] >= attrs['end_time']:
            raise serializers.ValidationError({'message': 'Start time must be earlier than end time'})

        if attrs['start_time'] < now():
            raise serializers.ValidationError({'message': 'Start time must be later than now'})

        return attrs

    def update(self, instance, validated_data):
        pass

    @transaction.atomic
    def create(self, validated_data):

        charging_socket: ChargingSocket = validated_data.pop('charging_socket')

        booked_item = charging_socket.make_booking(validated_data)

        if booked_item is None:
            raise serializers.ValidationError({'message': 'Charging socket is not available. Booking failed'})

        return booked_item
