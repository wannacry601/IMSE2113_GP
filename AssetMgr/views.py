from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions
from inspect import isclass
from django.shortcuts import render
from django.apps import apps
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout
from rest_framework import viewsets, permissions, views, mixins
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.utils.timezone import datetime
from .serializers import *
from . import models, forms
from django.contrib.auth import login, logout
import pandas

# the Django web application views
DEBUG = (permissions.AllowAny)
debug = True #Turn false when in production


# home = lambda request: render(request, 'blank.html')

def index(request):
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return render(request, "home.html", {"is_admin": True})
        return render(request, "home.html", {"is_admin": False})
    else:
        return redirect(app_login)

home = index

def how(request):
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return render(request, "how.html", {"is_admin": True})
        return render(request, "how.html", {"is_admin": False})
    else:
        return redirect(app_login)

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


def changeUser(request):
    pass

def addUser(request):
    return render(request, "add_user.html")
    
def addCargo(request):
    if request.method == 'POST':
        
        # queryset = (request.POST['is_in_warehouse'].__class__)
        # queryset = dict(request.POST)
        # queryset = {key: request.POST[key] for key in request.POST}
        # print(queryset.pop('csrfmiddlewaretoken').__class__)
        # print(queryset)
        # print(request.POST['is_in_warehouse'])#.__class__)
        # querydict = request.POST.__class__
        # print(querydict(queryset))
        form = forms.Cargo(request.POST)
        assert form.is_valid()
        print(form.cleaned_data)
        # form.save()
        models.Cargo(**form.cleaned_data).save()
        # assert form.is_valid(), "Form validation failed"
        
        # models.Cargo(form).save()
            # kwargs={'is_in_warehouse':{'on':True, 'off':False}[request.POST['is_in_warehouse']], 
            #     'on_pellet':int(request.POST['on_pellet']), 
            #     'destination':request.POST['destination'], 
            #     'arrival_date': datetime(*[int(i) for i in request.POST['arrival_date'].split('/')][::-1] + [0,0,0,0]), 
            #     'origin':request.POST['origin'],
            #     'due_outbound_date':datetime(*[int(i) for i in request.POST['due_outbound_date'].split('/')][::-1] + [0,0,0,0]), 
            #     'name':request.POST['name'],
            #     'desc':request.POST['desc'],
            #     'weight':int(request.POST['weight']),
            #     'caregory':request.POST['category']}
            # models.Cargo(kwargs).save()
        print(11)
        # if form.is_valid():
            # Cargo(form.cleaned_data).save()
        error = False
        # error = True
        return render(request, 'add_cargo.html', {'form': form, 'error':error})
    else:
        form = forms.Cargo()
        return render(request, 'add_cargo.html', {'form': form, 'error':2})

def changeCargo(request):
    pass

def search(request):
    try:
        query_string = request.GET['query_string']
    except KeyError:
        query_string = ''

    # try:
    #     search_type = request.GET['type']
    # except KeyError:
    #     search_type = 'name'
    search_type = 'name'
    query_string = query_string.strip()
    query_string = '.*' + query_string + '.*'
    if query_string == '':
        return render(request, 'search.html', {"queryset": None})

    if search_type == 'name':
        queryset = models.Cargo.objects.filter(name__regex=query_string)
        return render(request, 'search.html', {"queryset": queryset})

def inventoryReport(request):
    cargo_set = models.Cargo.objects.all()
    if request.method == "POST":
        filename = 'inventory_report' + str(datetime.now()).replace(" ", "_")
        df = pandas.DataFrame.from_records(cargo_set.values())
        response = HttpResponse(df.to_csv())
        response.headers['Content-Type'] = 'application/csv'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    else:
        return HttpResponse('Method not allowed!')

def userReport(request):
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
