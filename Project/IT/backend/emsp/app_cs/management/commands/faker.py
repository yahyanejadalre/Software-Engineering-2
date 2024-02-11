import random
import uuid
from datetime import timedelta, datetime
from typing import List, Tuple

from django.contrib.auth import get_user_model
from django.contrib.gis.geos import fromstr
from django.core.management import BaseCommand
from django.utils.timezone import make_aware
from django.utils.timezone import now
from faker import Faker

from app_booking.models import BookingHistory
from app_cs.models import ChargingStation, ChargingSocket

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = 'Generate fake data'

    def generate_sockets(self, station_count: int = 1_000):
        stations = []

        power_sources_list = list(ChargingStation.PowerSource.choices)
        socket_types = list(ChargingSocket.SocketType.choices)

        cs_count = ChargingStation.objects.count()

        if cs_count > 0:
            self.stdout.write(self.style.WARNING(
                f'ChargingStation table is already populated with {cs_count} charging stations. SKIPPED'))

        else:

            for _ in range(station_count):
                location = fromstr(f'POINT({fake.longitude()} {fake.latitude()})', srid=4326)
                price = random.randint(1, 20)
                power_source = random.choice(power_sources_list)[0]
                source_id = None

                if power_source in [ChargingStation.PowerSource.MIX, ChargingStation.PowerSource.DSO]:
                    source_id = str(uuid.uuid1())

                stations.append(
                    ChargingStation(location=location, price=price, source_id=source_id, power_source=power_source))

            stations = ChargingStation.objects.bulk_create(stations, batch_size=1000)

            self.stdout.write(self.style.SUCCESS(f'Successfully generated {len(stations)} stations data'))

        # Create fake charging sockets
        sockets = []
        done = []

        cs_count = ChargingSocket.objects.count()

        if cs_count > 0:
            self.stdout.write(self.style.WARNING(
                f'ChargingSocket table is already populated with {cs_count} charging sockets. SKIPPED'))

        else:

            if not stations:
                stations = ChargingStation.objects.all()

            for station in stations:

                if len(sockets) >= 1000:
                    done.extend(ChargingSocket.objects.bulk_create(sockets, batch_size=1000))
                    sockets = list()

                socket_count = random.randint(1, 8)
                for _ in range(socket_count):
                    sockets.append(ChargingSocket(type=random.choice(socket_types)[0], station=station))

            if sockets:
                done.extend(ChargingSocket.objects.bulk_create(sockets, batch_size=1000))

            self.stdout.write(self.style.SUCCESS(f'Successfully generated {len(sockets)} sockets data'))

        if not done:
            done = ChargingSocket.objects.all()

        return done

    def generate_users(self, input_users_count: int = 10_000):
        """
        generate faker user and populate db
        :return:
        """
        users = []
        users_count = User.objects.count()
        admin_accounts = User.objects.filter(is_superuser=True).count()
        if users_count > admin_accounts:
            self.stdout.write(self.style.WARNING(f'User table is already populated with {users_count} users. SKIPPED'))

        else:
            for _ in range(input_users_count):
                users.append(
                    User(username=fake.unique.user_name(), first_name=fake.first_name(), last_name=fake.last_name(),
                         email=fake.unique.email())
                )

            users = User.objects.bulk_create(users, batch_size=1000, ignore_conflicts=True)

            self.stdout.write(self.style.SUCCESS(f'Successfully generated {len(users)} users data'))

        return User.objects.exclude(is_superuser=True)

    def generate_booking_history(self, users: list, sockets: list, num_bookings: int = 10_000):

        _now = now()

        def generate_time_range(num_bookings: int) -> List[Tuple[datetime, datetime]]:
            time_range = []
            start_times = set()
            end_times = set()
            while len(time_range) < num_bookings:
                start_time = make_aware(fake.date_time_between(start_date='-30d', end_date=_now + timedelta(hours=15)))
                end_time = start_time + timedelta(hours=random.randint(1, 12))
                if start_time in start_times or end_time in end_times:
                    continue
                start_times.add(start_time)
                end_times.add(end_time)
                time_range.append((start_time, end_time))
            return time_range

        b_count = BookingHistory.objects.count()

        if b_count > 0:
            self.stdout.write(self.style.WARNING(
                f'BookingHistory table is already populated with {b_count} booking histories. SKIPPED'))

            return

        generated_times = generate_time_range(num_bookings=num_bookings)

        booking_list = []

        for start_time, end_time in generated_times:
            if len(booking_list) >= 10_000:
                BookingHistory.objects.bulk_create(booking_list, batch_size=1_000)
                booking_list = list()

            socket = random.choice(sockets)

            started_at = random.choice(
                [
                    None, make_aware(fake.date_time_between(start_date=start_time, end_date=end_time))
                ]
            )

            if not started_at and end_time > _now:
                status = BookingHistory.Status.EXPIRED

            elif started_at and end_time < _now:
                status = BookingHistory.Status.CHARGING

            elif started_at and end_time > _now:
                status = BookingHistory.Status.DONE

            else:
                status = BookingHistory.Status.BOOKED

            booking_list.append(
                BookingHistory(
                    user=random.choice(users),
                    charging_socket=socket,
                    start_time=start_time,
                    end_time=end_time,
                    charging_stared_at=started_at,
                    created_at=make_aware(fake.date_time_between(start_date='-60d', end_date=start_time)),
                    status=status,
                    price=((end_time - start_time).seconds // 3600) * socket.station.price
                )
            )

        if booking_list:
            BookingHistory.objects.bulk_create(booking_list, batch_size=1_000)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated {BookingHistory.objects.count()} booking history data'))

    def add_arguments(self, parser):
        parser.add_argument('--history', type=int, default=10_000)
        parser.add_argument('--user', type=int, default=10_000)
        parser.add_argument('--station', type=int, default=1_000)

    def handle(self, *args, **options):
        sockets = self.generate_sockets(max(options['station'], 0))
        users = self.generate_users(max(options['user'], 0))
        self.generate_booking_history(users, sockets, max(options['history'], 0))
