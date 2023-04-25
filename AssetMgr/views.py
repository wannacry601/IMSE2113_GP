from django.shortcuts import render, redirect
from django.utils.timezone import datetime
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from .serializers import *
from . import models, forms
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import pandas


# the Django web application views
home = lambda request: render(request, 'blank.html')

def how(request):
    return render(request, "how.html", {"is_admin": False})

def about(request):
    return render(request, 'about.html', {"is_admin": False})

def login(request):
    if request.method == "POST":
        user = request.user
        if user.is_authenticated:
            return redirect(home)
        else:
            try:
                username = request.POST['username']
                password = request.POST['password']
            except KeyError:
                return render(request, 'login.html', {'error': True})
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session.set_expiry(3600)
                try:
                    referer = request.META['HTTP_REFERER']
                except KeyError:
                    referer = None
                print(referer) # TODO
                if referer:
                    return redirect(referer)
            else:
                return render(request, 'login.html', {'error': True})

    else:
        return render(request, 'login.html', {'error': False})

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

def search(request):
    try:
        search_type = request.GET['type']
    except KeyError:
        search_type = 'cargo'
    if search_type == 'cargo':
        pass
        models.Cargo

def inventoryReport(request):
    cargo_set = models.Cargo.objects.all()
    if request.method == "POST":
        filename = str(datetime.now()).replace(" ", "_")
        df = pandas.DataFrame.from_records(cargo_set.values())
        response = HttpResponse(df.to_csv())
        response.headers['Content-Type'] = 'application/csv'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    else:
        pass

def userReport(request):
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