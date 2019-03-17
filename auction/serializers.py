from rest_framework import serializers
from . models import item, bids
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = item
        fields = ('id', 'name', 'desc', 'startTime', 'endTIme', 'startAmount', 'winner', 'imageUrl')
        
class ItemBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = item
        fields = ('id', 'name', 'desc', 'startTime', 'endTIme', 'startAmount', 'winner', 'imageUrl')

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = bids
        fields = ('id', 'bidder', 'article', 'amount', 'created', 'status')