import uuid
from typing import Union

from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as gis_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.db.models import Q, F

User = get_user_model()

__all__ = [
    'ChargingStation',
    'ChargingSocket'
]


class ChargingStation(models.Model):
    class PowerSource(models.TextChoices):
        DSO = ('DSO', 'DSO')
        BATTERY = ('Battery', 'Battery')
        MIX = ('Mix', 'Mix')

    location = gis_model.PointField()

    power_source = models.CharField(default=PowerSource.DSO, choices=PowerSource.choices, max_length=8)
    source_id = models.CharField(default=None, null=True, blank=False, max_length=256)
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    battery_level = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    vehicle_charged = models.PositiveBigIntegerField(default=0)

    class Meta:
        verbose_name = 'Charging Station'
        verbose_name_plural = 'Charging Stations'
        indexes = [
            models.Index(fields=['location'])
        ]

    def set_dso(self, source_id: str, price: int):
        self.power_source = ChargingStation.PowerSource.DSO
        self.source_id = source_id
        if price:
            self.price = price
        self.save(update_fields=['power_source', 'source_id', 'price'])

    def set_battery(self):
        self.power_source = ChargingStation.PowerSource.BATTERY
        self.source_id = None
        self.save(update_fields=['power_source', 'source_id'])

    def set_mix(self, source_id: str):
        self.power_source = ChargingStation.PowerSource.MIX
        self.source_id = source_id
        self.save(update_fields=['power_source', 'source_id'])

    def __str__(self):
        return f'{self.pk}: {self.location}'

    def __repr__(self):
        return self.__str__()


class ChargingSocket(models.Model):
    class SocketType(models.TextChoices):
        SLOW = ('Slow', 'slow')
        FAST = ('Fast', 'fast')
        RAPID = ('Rapid', 'rapid')

    is_charging = models.BooleanField(default=False)

    current_vehicle_charging_level = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0),
                                                                                        MaxValueValidator(100)])

    identifier = models.UUIDField(primary_key=True, default=uuid.uuid1)
    type = models.CharField(default=SocketType.FAST, choices=SocketType.choices, max_length=8)

    station = models.ForeignKey('ChargingStation', on_delete=models.CASCADE, related_name='stations',
                                related_query_name='stations')

    class Meta:
        verbose_name = 'Charging Socket'
        verbose_name_plural = 'Charging Sockets'

    def start_charging(self):

        if self.is_charging:
            return

        self.station.vehicle_charged = F('vehicle_charged') + 1
        self.station.save()
        self.is_charging = True
        self.save(update_fields=['is_charging'])

    def stop_charging(self):

        if not self.is_charging:
            return

        self.is_charging = False
        self.save(update_fields=['is_charging'])

    @transaction.atomic
    def make_booking(self, booking_data) -> Union[object, None]:
        """
        Make a booking for the charging socket
        :param booking_data:
        :return:
        """

        from app_booking.models import BookingHistory

        if not self.is_available(booking_data['start_time'], booking_data['end_time']):
            return None

        price = (booking_data['end_time'] - booking_data['start_time']).seconds // 3600 * self.station.price

        if price <= 0:
            price = self.station.price

        discount = self.station.discount

        price = price - (price * discount / 100)

        booking = BookingHistory.objects.create(
            user=booking_data['user'],
            start_time=booking_data['start_time'],
            end_time=booking_data['end_time'],
            charging_socket=self,
            price=price,
        )
        return booking

    def is_available(self, start_time, end_time) -> bool:
        """
        Check if the charging socket is available for booking at the given time range
        :param start_time:
        :param end_time:
        :return:
        """

        from app_booking.models import BookingHistory

        booked_history = BookingHistory.objects.filter(
            Q(start_time__lte=start_time, end_time__gte=start_time) |
            Q(start_time__lte=end_time, end_time__gte=end_time) |
            Q(start_time__gte=start_time, end_time__lte=end_time),
            charging_socket=self,
            status__in=(BookingHistory.Status.BOOKED, BookingHistory.Status.CHARGING),
        )

        return not booked_history.exists()

    def __str__(self):
        return f'[{self.station}] {self.identifier}: {self.type}'

    def __repr__(self):
        return self.__str__()
