from django.shortcuts import render
from django.contrib.auth import login, logout
from rest_framework import viewsets, permissions, views
from rest_framework.response import Response
from .serializers import *
from . import models

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