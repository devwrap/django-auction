from django.shortcuts import render
from django.db.models import Max
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import item, bids
from .serializers import UserSerializer, ItemSerializer, BidSerializer
from datetime import date, datetime

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ItemView(viewsets.ModelViewSet):
    queryset = item.objects.all()
    serializer_class = ItemSerializer
    
    #this will return bids for item according to its auction status
    @action(methods=['get'], detail=True)
    def get_status(self, request, pk=None):
        itemDetail = self.get_queryset().get(pk=pk)
        if datetime.now().timestamp() < itemDetail.endTIme.timestamp() and datetime.now().timestamp() > itemDetail.startTime.timestamp():
            val = bids.objects.filter(article_id=itemDetail.id, status='valid').aggregate(Max('amount'))
            bid = bids.objects.filter(article_id=itemDetail.id, amount= float(val['amount__max']), status='valid').first()
            serialise = BidSerializer(bid)
            return Response({'Success': 'Item is still under auction, here is max bid till now', 'data':serialise.data}, status=status.HTTP_200_OK)
        if datetime.now().timestamp() > itemDetail.endTIme.timestamp():
            serialise = self.get_serializer.get(itemDetail.winner)
            return Response({'Success': 'Item is done with auction, here is the winning bid', 'data':serialise.data}, status=status.HTTP_200_OK)
        if datetime.now().timestamp() < itemDetail.startTime.timestamp():
            return Response({'Success': 'Item auction is yet to start'}, status=status.HTTP_200_OK)

    # this will return valid bids for an item
    @action(methods=['get'], detail=True)
    def get_bids(self, request, pk=None):
        bid = bids.objects.filter(article_id=self.get_queryset().get(pk=pk).id, status='valid')
        serialise = BidSerializer(bid, many=True)
        return Response(serialise.data)
    
    # to get items under auction currently
    @action(methods=['get'], detail=False)
    def auction_curr(self, request):
        item = self.get_queryset().filter(startTime__lte=datetime.today(), endTIme__gte=datetime.today())
        serialise = self.get_serializer(item, many=True)
        return Response(serialise.data, status=status.HTTP_200_OK)
        
    # to get items done with auction
    @action(methods=['get'], detail=False)
    def auction_complete(self,request):
        item = self.get_queryset().filter(endTIme__lt=datetime.today())
        serialise = self.get_serializer(item, many=True)
        return Response(serialise.data, status=status.HTTP_200_OK)

    # to get items with auction yet to happen
    @action(methods=['get'], detail=False)
    def auction_upcoming(self, request):
        item = self.get_queryset().filter(startTime__gt=datetime.today())
        serialise = self.get_serializer(item, many=True)
        return Response(serialise.data, status=status.HTTP_200_OK)

    # get all the items whos auction time ended toda
    @action(methods=['get'], detail=False)
    def shceduled_job_test(self):
        itemList = item.objects.filter(endTIme=date.today()).filter(endTIme__lt=datetime.now())
        for i in itemList:
            val = bids.objects.filter(status='valid', article_id=i.id).aggregate(Max('amount'))
            bid = bids.objects.filter(article_id=itemDetail.id, amount= float(val['amount__max']), status='valid').first()
            i.winner = bid.bidder
            i.save()
        return Response({'Success': 'Item auction is yet to start'}, status=status.HTTP_200_OK)

class BidView(viewsets.ModelViewSet):
    queryset = bids.objects.all()
    serializer_class = BidSerializer

    def create(self, request):
        data = request.data
        serializer = BidSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            check = item.objects.get(id=data['article'])
            bid = bids.objects.all().last()
            if check.endTIme.timestamp() > datetime.now().timestamp() and datetime.now().timestamp() > check.startTime.timestamp():
                bid.status = 'valid'
                bid.save()
            else:
                bid.status = 'invalid'
                bid.save()
            serializer = BidSerializer(bid)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)