from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from datetime import datetime, timedelta
from .models import *

last_ditch = lambda request: render(request, 'site_dead.html' )
# This is only for testing, last_ditch() should NOT be used.

def gatekeeper(request, staff_only=False): return None if ((request.user.is_authenticated and request.user.is_staff) if staff_only else request.user.is_authenticated) else render(request, 'login.html', {'staffOnly': True} if staff_only else {'UsersOnly': True}, status = 403)

def user_management(request):
    if not_auth := gatekeeper(request): return not_auth
    is_prole = bool(gatekeeper(request, True))
    users = User.objects.filter(id = request.user.id) if is_prole else user_select(request)
    if request.method == 'GET': return render(request, 'user_management.html', {'users': users} if not users['error'] else users, status = 200 if not users['error'] else 400)
    new_username, old_password, new_password, new_email, new_first_name, new_last_name = map(request.POST.get, ['username', 'current_password', 'password', 'email', 'first_name', 'last_name'])
    if not check_password(old_password, current_user_password := User.objects.filter(id = request.user.id).password): return render(request, 'manage_user.html', {'badPassword': True}, status = 400)
    if new_password == '': new_password = old_password
    new_user = User(id = request.user.id if is_prole else request.POST.get('selected_user'),\
                    username = new_username if new_username else request.user.username,\
                    password = new_password,\
                    email = new_email if new_email else request.user.email,\
                    first_name = new_first_name if new_first_name else request.user.first_name,\
                    last_name = new_last_name if new_last_name else request.user.last_name)
    new_user.save()
    return render(request, 'user_management.html')

def user_select(request): 
    if not_auth := gatekeeper(request, True): return not_auth
    filters, params = map(request.POST.get,['filters', params])
    if sum(bool(screen for screen in filters)) > 1: return {'TooManyRequests': True, 'Error': True}
    match filters:
        case 'name': return User.objects.filter(name = params)
        case 'user_id': return User.objects.filter(id = params)
        case 'email': return User.objects.filter(email = params)

def receive_pellet(request):
    if not_auth := gatekeeper(request): return not_auth
    if request.method != 'POST':
         pellet = Pellet.objects.filter(is_inbound = True).order_by('-inbound_shipment')
         return render(request, 'receive_package.html', {'received_pellets': pellet, 'string_rep_of_pellet': str(pellet)}) 
    column, row, pellet_name, pellet_desc = map(request.POST.get, ['column', 'row', 'name', 'description'])
    new_received_pellet = Pellet(is_inbound = True, column = column, row = row, pellet_name = pellet_name, pellet_desc = pellet_desc)
    try:
        new_received_pellet.save()
        return render(request, 'receive_package.html', {'success': True}, status = 409)
    except IntegrityError as IE:
        return render(request, 'receive_package.html', {'SpaceAlreadyOccupied': True, 'name': pellet_name, 'desc': pellet_desc})

def build_order(request):
    if not_auth := gatekeeper(request): return not_auth
    if request.method == 'GET': return render(request, 'orders.html', {'orders': Order.objects.all()})
    due_date, order_type, quantity, destination, title, description = map(request.POST.get, ['due_date', 'type', 'quantity', 'destination', 'title', 'description'])
    order = Order(due_date = due_date, order_type = order_type, quantity = quantity, destination = destination, title = title, description = description)
    order.save()
    return render(request, 'build_orders.html', {'Order': order})

def shipment_outbound(request):
    if not_auth := gatekeeper(request): return not_auth
    if request.GET.get('build_new_shipment'): return render(request, 'build_a_shipment.html')
    elif request.method == 'GET': return render(request, 'outbound_shipments.html', {'shipments': Outbound.objects.all()})
    shipment_date, desc, dest = map(request.POST.get, ['date', 'desc', 'dest'])
    new_shipment_outbound = Outbound(shipment_date = shipment_date, desc = desc, dest = dest)
    try:
        new_shipment_outbound.save()
        return render(request, 'build_a_shipment.html', {'shipment_id': new_shipment_outbound.id, 'shipment_str': str(new_shipment_outbound), 'overdue_shipments': Order.objects.filter(date__lt = shipment_date), 'close_to_due': Order.objects.filter(date__range = [start := datetime.strptime(shipment_date, '%Y-%m-%d').date(), start + timedelta(days = 14)])})
    except IntegrityError as IE:
        return render(request, 'build_a_shipment.html', {'ShipmentAlreadyExists': True})
# Create your views here.
