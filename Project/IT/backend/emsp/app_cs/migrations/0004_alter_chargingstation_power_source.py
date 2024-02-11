# Generated by Django 4.1.5 on 2023-01-18 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_cs', '0003_chargingstation_source_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chargingstation',
            name='power_source',
            field=models.CharField(choices=[('DSO', 'DSO'), ('Battery', 'Battery'), ('Mix', 'Mix')], default='DSO', max_length=8),
        ),
    ]
