from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator

class Panel(models.Model):
    brand = models.CharField(max_length=200)
    serial = models.CharField(
        max_length=200,
        validators=[
            RegexValidator(regex='^.{16}$',
                        message='Length has to be 16.',
                        code='nomatch')
        ])
    latitude = models.DecimalField(decimal_places=6,max_digits=8)
    longitude = models.DecimalField(decimal_places=6,max_digits=9)
    def __str__(self):
        return "Brand: {0}, Serial: {1} ".format(self.brand, self.serial)

class OneHourElectricity(models.Model):
    panel = models.ForeignKey(Panel, on_delete=models.CASCADE)
    kilo_watt = models.BigIntegerField(validators=[MinValueValidator(1)])
    date_time = models.DateTimeField()
    def __str__(self):
        return "Hour: {0} - {1} KiloWatt".format(self.date_time, self.kilo_watt)
