from django.db import models


class Car(models.Model):
    make = models.CharField(max_length=128)
    model = models.CharField(max_length=128)


class Rating(models.Model):
    value = models.FloatField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
