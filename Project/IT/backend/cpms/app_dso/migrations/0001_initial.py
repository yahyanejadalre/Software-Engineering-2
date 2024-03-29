# Generated by Django 4.1.5 on 2023-02-03 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DSO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=256)),
                ('price', models.PositiveBigIntegerField()),
                ('name', models.CharField(max_length=255)),
                ('is_available', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'DSO',
                'verbose_name_plural': 'DSOs',
                'ordering': ('-updated_at',),
            },
        ),
    ]
