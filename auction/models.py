from django.db import models
from django.contrib.auth.models import User
from datetime import date

# class user(models.Model):
#     name = models.CharField(max_length=50)
#     email = models.EmailField()
#     password = models

class item(models.Model):
    name = models.CharField(max_length=20)
    desc = models.CharField(max_length=50)
    startTime = models.DateTimeField()
    endTIme = models.DateTimeField()
    startAmount = models.FloatField()
    winner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    imageUrl = models.URLField()

class bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(item, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    status = models.CharField(max_length=10, null=True)
