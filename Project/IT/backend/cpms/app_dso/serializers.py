from rest_framework import serializers

from app_dso.models import DSO


class DSOModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DSO
        fields = '__all__'
