import uuid

from django.contrib.auth import get_user_model
from django.db import models

from app_cs.models import ChargingSocket

User = get_user_model()

__all__ = [
    'BookingHistory',
]


class BookingHistory(models.Model):
    class Status(models.TextChoices):
        BOOKED = ('Booked', 'Booked')
        CHARGING = ('Charging', 'Charging')
        EXPIRED = ('Expired', 'Expired')
        DONE = ('Done', 'Done')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    status = models.CharField(choices=Status.choices, default=Status.BOOKED, max_length=16)
    charging_socket = models.ForeignKey(ChargingSocket, on_delete=models.PROTECT, related_name='sockets',
                                        related_query_name='sockets')

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    charging_stared_at = models.DateTimeField(null=True, blank=True)

    unique_code = models.UUIDField(unique=True, default=uuid.uuid1)
    price = models.PositiveBigIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Booking History'
        verbose_name_plural = 'Booking Histories'

        ordering = [
            '-created_at'
        ]

        indexes = [
            models.Index(fields=['start_time', 'end_time', 'charging_socket', 'status'])
        ]

    def __str__(self):
        return f'[{self.status}] {self.charging_socket.identifier}, from {self.start_time} to {self.end_time}'

    def __repr__(self):
        return self.__str__()
