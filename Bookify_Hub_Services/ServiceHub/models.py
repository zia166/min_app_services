from django.db import models

# Create your models here.
class Event(models.Model):
    username = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

 
