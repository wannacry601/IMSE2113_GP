from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import *
from . import models

home = lambda request: render(request, 'blank.html')

class Userviewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class CargoViewset(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    permission_classes = [permissions.IsAuthenticated]

class InboundViewset(viewsets.ModelViewSet):
    queryset = Inbound.objects.all()
    serializer_class = InboundSerializer
    permission_classes = [permissions.IsAuthenticated]

class OutboundViewset(viewsets.ModelViewSet):
    queryset = Outbound.objects.all()
    serializer_class = OutboundSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductsViewset(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [permissions.IsAuthenticated]

class PelletViewset(viewsets.ModelViewSet):
    queryset = Pellet.objects.all()
    serializer_class = PelletSerializer
    permission_classes = [permissions.IsAuthenticated]