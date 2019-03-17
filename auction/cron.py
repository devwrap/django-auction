from rest_framework import viewsets, status
from django.db.models import Max
from django.db.models import Avg
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import item, bids
from .serializers import UserSerializer, ItemSerializer, BidSerializer
from datetime import date, datetime


def shceduled_job():
    # get all the items whos auction time ended today
    # for each item's auction ended today, calculate winner
    itemList = item.objects.filter(endTIme=date.today()).filter(endTIme__lt=datetime.now())
    for i in itemList:
        val = bids.objects.filter(status='valid', article_id=i.id).aggregate(Max('amount'))
        bid = bids.objects.filter(article_id=itemDetail.id, amount= float(val['amount__max']), status='valid').first()
        i.winner = bid.bidder
        i.save()