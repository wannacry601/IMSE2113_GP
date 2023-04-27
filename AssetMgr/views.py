from inspect import isclass
from django.shortcuts import render
from django.apps import apps
from django.contrib.auth import login, logout
from rest_framework import viewsets, permissions, views, mixins
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .serializers import *
from . import models

DEBUG = (permissions.AllowAny)
debug = True #Turn false when in production


home = lambda request: render(request, 'blank.html')

class Userviewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer   

class CargoViewset(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ProductsViewset(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

class PelletViewset(viewsets.ModelViewSet):
    queryset = Pellet.objects.all()
    serializer_class = PelletSerializer

class LoginViewset(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
        context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({'message': 'successfully logged in', 'auth': True}, status=202)

class LogoutViewset(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out', 'auth': False})
        

class CheckAuth(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        return Response({'is_authenticated': request.user.is_authenticated})


class AllDataViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = DEBUG if debug else (permissions.IsAuthenticated)
    def list(self, request, *args, **kwargs):
        data = {}

        # Retrieve data for User
        queryset1 = User.objects.all()
        serializer1 = UserSerializer(queryset1, many=True, context={'request': request})
        data['user_data'] = serializer1.data

        # Retrieve data for Cargo
        queryset2 = Cargo.objects.all()
        serializer2 = CargoSerializer(queryset2, many=True, context={'request': request})
        data['cargo_data'] = serializer2.data

        # Retrieve data for Order
        queryset3 = Order.objects.all()
        serializer3 = OrderSerializer(queryset3, many=True, context={'request': request})
        data['order_data'] = serializer3.data

        # Retrieve data for Products
        queryset4 = Products.objects.all()
        serializer4 = ProductsSerializer(queryset4, many=True, context={'request': request})
        data['products_data'] = serializer4.data

        # Retrieve data for Pellet
        queryset5 = Pellet.objects.all()
        serializer5 = PelletSerializer(queryset5, many=True, context={'request': request})
        data['pellet_data'] = serializer5.data

        return Response(data)