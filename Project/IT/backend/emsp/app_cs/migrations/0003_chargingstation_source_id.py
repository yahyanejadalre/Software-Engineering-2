# Generated by Django 4.1.5 on 2023-01-18 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_cs', '0002_chargingstation_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='chargingstation',
            name='source_id',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
    ]
