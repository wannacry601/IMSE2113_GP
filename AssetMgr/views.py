from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions
from .serializers import *
from . import models, forms
from django.contrib.auth import login, logout

# the Django web application views
home = lambda request: render(request, 'blank.html')

def how(request):
    return render(request, "how.html", {"is_admin": False})

def about(request):
    return render(request, 'about.html', {"is_admin": False})

def login(request):
    if request.method == "POST":
        request.POST
        request.session.set_expiry(3600)
    else:
        return render(request, 'login.html')

def logout(request):
    if request.method == "POST":
        user = request.user
        if user.is_authenticated:
            logout(user)
            return redirect(home)
    else:
        pass

def disable(request):
    
    pass

def changeUser(request):
    pass

def addUser(request):
    return render(request, "add_user.html")
    pass

# end of Django web application views

# start of Django rest framework views
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

# end of Django rest framework views