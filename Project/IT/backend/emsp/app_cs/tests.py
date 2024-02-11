from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.gis.geos import fromstr
from django.test import TestCase
from faker import Faker
from django.utils.timezone import make_aware
from app_cs import models as cs_models

User = get_user_model()

fake = Faker()


class BookingsTest(TestCase):

    def setUp(self) -> None:
        self.user_data = {
            'username': 'test_user@email.com',
            'password': 'test_password',
            'email': 'test_user@email.com',
            'first_name': 'test',
            'last_name': 'user'
        }

        self.user = User.objects.create_user(**self.user_data)
        self.user.set_password(self.user_data['password'])

        self.charging_station = cs_models.ChargingStation.objects.create(
            price=100,
            location=fromstr(f'POINT({fake.longitude()} {fake.latitude()})', srid=4326),
            discount=10,
            vehicle_charged=10,
            battery_level=50,
            power_source=cs_models.ChargingStation.PowerSource.BATTERY,
        )

        self.charging_socket = cs_models.ChargingSocket.objects.create(
            station=self.charging_station
        )

        self.book_data = {
            'user': self.user,
            'charging_socket': self.charging_socket,
            'start_time': make_aware(datetime.fromisoformat('2021-01-01 00:00:00')),
            'end_time': make_aware(datetime.fromisoformat('2021-01-01 03:00:00')),
        }

        self.valid_booking_data = {
            'user': self.user,
            'charging_socket': self.charging_socket,
            'start_time': make_aware(datetime.fromisoformat('2021-01-01 03:00:01')),
            'end_time': make_aware(datetime.fromisoformat('2021-01-01 04:00:00')),
        }

        self.invalid_booking_data = {
            'user': self.user,
            'charging_socket': self.charging_socket,
            'start_time': make_aware(datetime.fromisoformat('2021-01-01 00:00:00')),
            'end_time': make_aware(datetime.fromisoformat('2021-01-01 03:00:00')),
        }

        self.charging_socket.make_booking(self.book_data)

    def test_valid_booking(self):
        booking = self.charging_socket.make_booking(self.valid_booking_data)
        self.assertIsNotNone(booking)

    def test_invalid_booking(self):
        booking = self.charging_socket.make_booking(self.invalid_booking_data)
        self.assertIsNone(booking)
