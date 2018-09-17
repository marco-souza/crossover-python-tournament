from rest_framework import serializers
from django.db import models
from .models import Panel, OneHourElectricity

class PanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panel
        fields = ('id', 'brand', 'serial', 'latitude', 'longitude')

class OneHourElectricitySerializer(serializers.ModelSerializer):
    class Meta:
        panel = serializers.PrimaryKeyRelatedField(queryset=Panel.objects.all())
        model = OneHourElectricity
        fields = ('id', 'panel', 'kilo_watt','date_time')


class DayElectricity(models.Model):
    date_time = models.DateTimeField()
    sum = models.FloatField()
    average = models.FloatField()
    maximum = models.FloatField()
    minimum = models.BigIntegerField()
    def __str__(self):
        return "Date: {0} - (sum: {1}, avg: {2}, max: {3}, min: {4})"\
            .format(self.date_time, self.sum,
                    self.average, self.maximum, self.maximum)


class DayElectricitySerializer(serializers.ModelSerializer):

    class Meta:
        model = DayElectricity
        fields = ('date_time', 'sum', 'average', 'maximum', 'minimum')