import uuid

from django.db import models


class DSO(models.Model):
    identifier = models.CharField(max_length=256, unique=True, default=uuid.uuid1)
    price = models.PositiveBigIntegerField()
    name = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)

    active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'DSO'
        verbose_name_plural = 'DSOs'
        ordering = ('-updated_at',)

    def __str__(self):
        return f'{self.name}: is_available={self.is_available}, price={self.price}'
