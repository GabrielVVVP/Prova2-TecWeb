from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200) 
    password = models.CharField(max_length=200)
    favorites = models.CharField(max_length=200, null=True)
    def __str__(self):
        return str(self.id)+"."+self.name   

class Station(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200,default="-8.093178907962578,-34.88296508789063")
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.id)+"."+self.name     

class Parameter(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    readings = models.TextField(default="")
    dates = models.TextField(default="")
    location = models.CharField(max_length=200,default="-8.093178907962578,-34.88296508789063")
    def __str__(self):
        return self.station.name+"."+self.name
