from django.core.management import BaseCommand
from django.db import transaction
from faker import Faker

from app_dso.models import DSO

fake = Faker()

DSO_COUNT = 10


class Command(BaseCommand):
    help = 'Generate fake data'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=DSO_COUNT)

    def handle(self, *args, **options):

        DSO_COUNT = max(options['count'], 1)

        if count := DSO.objects.count():
            self.stdout.write(self.style.WARNING(f'{count} DSO objects already exist'))
            return

        self.stdout.write(f'Generating {DSO_COUNT} fake DSOs...')

        dso_list = []
        for _ in range(DSO_COUNT):
            dso_list.append(
                DSO(
                    identifier=fake.unique.uuid4(),
                    price=fake.random_int(min=1, max=1000),
                    name=fake.name(),
                    is_available=fake.boolean(),
                )
            )
        with transaction.atomic():
            DSO.objects.bulk_create(dso_list)
            dso = DSO.objects.order_by('?').first()
            dso.active = True
            dso.is_available = True
            dso.save(update_fields=['active', 'is_available'])

        self.stdout.write(self.style.SUCCESS(f'{DSO_COUNT} fake DSOs were generated'))
