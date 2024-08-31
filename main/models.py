from django.db import models

class Compares(models.Model):
    username1 = models.CharField(max_length=22)
    username2 = models.CharField(max_length=22)
    percentage = models.IntegerField()
    

# Create your models here.
