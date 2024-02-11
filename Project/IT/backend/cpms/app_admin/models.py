from django.core.exceptions import ImproperlyConfigured
from django.db import models


def get_system_config(key, default=None):
    if config := SystemConfig.objects.filter(key__iexact=key).first():
        return config.casted_value
    else:
        if default is None:
            raise ImproperlyConfigured(f'No system config found for {key}')
        return default


class SystemConfig(models.Model):
    class Types(models.TextChoices):
        integer = ('int', 'int')
        string = ('str', 'str')
        boolean = ('bool', 'bool')

    key = models.CharField(max_length=128, primary_key=True)
    value = models.CharField(max_length=256)
    value_type = models.CharField(default=Types.string, choices=Types.choices, max_length=8)

    editable = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=False, help_text='is visible to normal user')

    help_text = models.CharField(max_length=256, null=True, blank=True)

    update_at = models.DateTimeField(auto_now=True)

    @property
    def casted_value(self):

        if self.value_type == self.Types.boolean:
            return self.value.lower() == 'true'

        import builtins
        cast_function = getattr(builtins, self.value_type)
        return cast_function(self.value)

    @staticmethod
    def add_config(key: str, value):
        if type(value) == int:
            _type = SystemConfig.Types.integer
        elif type(value) == bool:
            _type = SystemConfig.Types.boolean
        else:
            _type = SystemConfig.Types.string

        _value = str(value)

        instance, _ = SystemConfig.objects.get_or_create(key=str(key), value=_value, value_type=_type)

        return instance

    def __str__(self):
        return f'{self.key}: {self.value}'


