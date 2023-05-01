import sqlite3
from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions
from inspect import isclass
from django.shortcuts import render
from django.apps import apps
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, views, mixins
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.utils.timezone import datetime
from .serializers import *
from . import models, forms
from django.contrib.auth import decorators
from django.contrib.auth import login, logout
import pandas
import qrcode
import json

# the Django web application views
DEBUG = (permissions.AllowAny)
debug = True #Turn false when in production


# home = lambda request: render(request, 'blank.html')
# @decorators.login_required("/login/")
def index(request):
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return render(request, "home.html", {"is_admin": True})
        return render(request, "home.html", {"is_admin": False})
    else:
        return redirect(app_login)

home = index

# @decorators.login_required("/login/")
def how(request):
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return render(request, "how.html", {"is_admin": True})
        return render(request, "how.html", {"is_admin": False})
    else:
        return redirect(app_login)

# @decorators.login_required("/login/")
def about(request):
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return render(request, "about.html", {"is_admin": True})
        return render(request, "about.html", {"is_admin": False})
    else:
        return redirect(app_login)

def app_login(request):
    empty_form = forms.LoginForm()
    if request.method == "POST":
        user = request.user
        if user.is_authenticated:
            return redirect(index)
        else:
            try:
                username = request.POST['username']
                password = request.POST['password']
            except KeyError:
                return render(request, 'login.html', {'error': True, 'form': empty_form})
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session.set_expiry(3600)
                try:
                    referer = request.META['HTTP_REFERER']
                except KeyError:
                    referer = None
                if referer:
                    return redirect(referer)
                else: 
                    return redirect(home)
            else:
                return render(request, 'login.html', {'error': True})
    else:
        return render(request, 'login.html', {'error': False, 'form': empty_form})

# @decorators.login_required("/login/")
def app_logout(request):
    if request.method == "POST":
        user = request.user
        if user.is_authenticated:
            logout(user)
            return redirect(home)
        else:
            try:
                referer = request.META['HTTP_REFERER']
            except KeyError:
                referer = None
            if referer:
                return HttpResponseRedirect(referer)
            else:
                return HttpResponseRedirect('about/')
    else:
        return redirect(home)

# @decorators.login_required("/login/")
def changeUser(request,userid):

    current_user = request.user
    if not current_user.is_authenticated:
        return redirect(app_login)
    idlist = [
            'auth_token', 
            'date_joined', 
            'email', 
            'first_name', 
            'groups', 
            'id',
            'is_active', 
            'is_staff', 
            'is_superuser', 
            'last_login', 
            'last_name', 
            'logentry', 
            'password', 
            'user_permissions', 
            'username'
        ]
    implementdata = dict()
    if request.method == "GET":
        userinf = list(User.objects.filter(id=userid).values_list(
            'auth_token', 
            'date_joined', 
            'email', 
            'first_name', 
            'groups', 
            'id',
            'is_active', 
            'is_staff', 
            'is_superuser', 
            'last_login', 
            'last_name', 
            'logentry', 
            'password', 
            'user_permissions', 
            'username'))
        for i in range(len(idlist)): implementdata[idlist[i]]=userinf[0][i]
        print(implementdata)
        return render(request,'user_manage.html',{"infos":implementdata})
    if request.method == "POST":
        updated_data = dict()
        for column in idlist: updated_data[column] = request.POST.get(f'{column}')
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        for column in updated_data: cursor.execute(f"UPDATE auth_user SET {column}=\'{updated_data[column]}\' WHERE id = \'{request.user.id}\'")
        cursor.close()
        conn.commit()
        return HttpResponseRedirect('/')


# @decorators.login_required("/login/")
def addUser(request):
    current_user = request.user
    if not current_user.is_authenticated:
        return redirect(app_login)
    
    if not current_user.is_superuser:
        return render(request, 'add_user.html', {'error':3})

    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            User(**form.cleaned_data).save()
            error = False
        else: error = True
        return render(request, 'add_user.html', {'form': form, 'error':error})
    else:
        form = forms.SignUpForm()
        return render(request, 'add_user.html', {'form': form, 'error':2})

# @decorators.login_required("/login/")  
def addCargo(request):

    current_user = request.user
    if not current_user.is_authenticated:
        return redirect(app_login)

    if request.method == 'POST':
        form = forms.Cargo(request.POST)
        if form.is_valid():
            models.Cargo(**form.cleaned_data).save()
            error = False
        else: error = True
        return render(request, 'add_cargo.html', {'form': form, 'error':error})
    else:
        form = forms.Cargo()
        return render(request, 'add_cargo.html', {'form': form, 'error':2})

# @decorators.login_required("/login/")  
def changeCargo(request,cargoid):

    current_user = request.user
    if not current_user.is_authenticated:
        return redirect(app_login)
    implementdata = dict()
    idlist = ['is_in_warehouse',
            'on_pellet',
            'destination',
            'arrival_date',
            'origin',
            'due_outbound_date',
            'name',
            'id',
            'desc',
            'weight',
            'category'
        ]
    if request.method == "GET":
        cargoinf = list(Cargo.objects.filter(id=cargoid).values_list(
            'is_in_warehouse',
            'on_pellet',
            'destination',
            'arrival_date',
            'origin',
            'due_outbound_date',
            'name',
            'id',
            'desc',
            'weight',
            'category'
        ))
        for i in range(len(idlist)): implementdata[idlist[i]]=cargoinf[0][i]
        return render(request,'cargo_manage.html',{"infos":implementdata})
    if request.method == "POST":
        updated_data = dict()
        for column in idlist:
            if (column=="on_pellet" or column=="category"):updated_data[column+"_id"] = request.POST.get(f'{column}')
            else:updated_data[column] = request.POST.get(f'{column}')
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        id = updated_data['id']
        for column in updated_data:
            print(column)
            print(updated_data[column])
            cursor.execute(f"UPDATE AssetMgr_Cargo SET {column}=\'{updated_data[column]}\' WHERE id = \'{id}\'")
        cursor.close()
        conn.commit()
        return HttpResponseRedirect('/')
        
    

# @decorators.login_required("/login/")
def search(request):

    current_user = request.user
    if not current_user.is_authenticated:
        return redirect(app_login)

    try:
        query_string = request.GET['query_string']
    except KeyError:
        query_string = ''

    try:
        search_type = request.GET['type']
    except KeyError:
        search_type = None

    form = forms.SearchForm()

    if not search_type:
        return render(request, 'search.html', {'form': form, 'found': True})

    query_string = query_string.strip()
    query_string = '.*' + query_string + '.*'
    if query_string == '':
        return render(request, 'search.html', {'found': False})

    if search_type == 'name':
        queryset = models.Cargo.objects.filter(name__regex=query_string)
        return render(request, 'search.html', {"queryset": queryset, 'found': True})
    if search_type == 'id':
        queryset = models.Cargo.objects.filter(id__regex=query_string)
        return render(request, 'search.html', {"queryset": queryset, 'found': True})
    if search_type == 'destination':
        queryset = models.Cargo.objects.filter(destination__regex=query_string)
        return render(request, 'search.html', {"queryset": queryset, 'found': True})
    if search_type == 'desc':
        queryset = models.Cargo.objects.filter(desc__regex=query_string)
        return render(request, 'search.html', {"queryset": queryset, 'found': True})
    return render(request, 'search.html', {'found': True, 'form':form})

# @decorators.login_required("/login/")
def inventoryReport(request):

    current_user = request.user
    if not current_user.is_authenticated:
        return redirect(app_login)

    cargo_set = models.Cargo.objects.all()
    if request.method == "POST":
        filename = 'inventory_report' + str(datetime.now()).replace(" ", "_")
        df = pandas.DataFrame.from_records(cargo_set.values())
        response = HttpResponse(df.to_csv())
        response.headers['Content-Type'] = 'application/csv'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    else:
        return HttpResponse('Method not allowed!')

# @decorators.login_required("/login/")
def userReport(request):

    current_user = request.user
    if not current_user.is_authenticated:
        return redirect(app_login)

    user_set = User.objects.all()
    if request.method == "POST":
        filename = 'user_report' + str(datetime.now()).replace(" ", "_")
        df = pandas.DataFrame.from_records(user_set.values())
        response = HttpResponse(df.to_csv())
        response.headers['Content-Type'] = 'application/csv'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    else:
        return HttpResponse('Method not allowed!')



# end of Django web application views

# start of Django rest framework views
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
    permission_classes = [permissions.IsAuthenticated]

# end of Django rest framework views

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
