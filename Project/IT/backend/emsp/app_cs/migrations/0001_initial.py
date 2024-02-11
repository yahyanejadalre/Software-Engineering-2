# Generated by Django 4.1.5 on 2023-01-13 16:27

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChargingSocket',
            fields=[
                ('identifier', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('Slow', 'slow'), ('Fast', 'fast'), ('Rapid', 'rapid')], default='Fast', max_length=8)),
            ],
            options={
                'verbose_name': 'Charging Socket',
                'verbose_name_plural': 'Charging Sockets',
            },
        ),
        migrations.CreateModel(
            name='ChargingStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('power_source', models.CharField(choices=[('DSO', 'DSO'), ('Battery', 'Battery')], default='DSO', max_length=8)),
                ('price', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'Charging Station',
                'verbose_name_plural': 'Charging Stations',
            },
        ),
        migrations.AddIndex(
            model_name='chargingstation',
            index=models.Index(fields=['location'], name='app_cs_char_locatio_d0fa4d_idx'),
        ),
        migrations.AddField(
            model_name='chargingsocket',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stations', related_query_name='stations', to='app_cs.chargingstation'),
        ),
    ]