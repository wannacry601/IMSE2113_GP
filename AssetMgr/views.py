# from django.shortcuts import render
# from django.db import IntegrityError
# from django.contrib.auth.models import User
# from django.contrib.auth.hashers import check_password
# from datetime import datetime, timedelta
# from .models import *


# def gatekeeper(request, staff_only=False): return None if ((request.user.is_authenticated and request.user.is_staff) if staff_only else request.user.is_authenticated) else render(request, 'login.html', {'staffOnly': True} if staff_only else {'UsersOnly': True}, status = 403)\
# #This function deals with checking if the user is authenticated, or is staff.
# #It returns users to LOGIN.HTML if they are not authorised.

# def user_management(request):
#     #Function to fetch and amend existing users.
#     if not_auth := gatekeeper(request): return not_auth
#     # This just checks if they're authenticated. You'll see this incantation a lot.
#     is_prole = bool(gatekeeper(request, True))
#     # True for staff, False for regular users
#     users = User.objects.filter(id = request.user.id) if is_prole else user_select(request)
#     if request.method == 'GET': return render(request, 'user_management.html', {'users': users} if not users['error'] else users, status = 200 if not users['error'] else 400)
#     new_username, old_password, new_password, new_email, new_first_name, new_last_name = map(request.POST.get, ['username', 'current_password', 'password', 'email', 'first_name', 'last_name'])
#     # Using the map() function, pulling from the keys ['username', 'current_password', 'password', 'email', 'first_name', 'last_name']
#     if not check_password(old_password, current_user_password := User.objects.filter(id = request.user.id).password): return render(request, 'manage_user.html', {'badPassword': True}, status = 400)
#     #MANDATORY password checking: Old passwords must match for ANY check
#     #HTTP 400: Bad Request will be returned if pwd mismatch
#     if new_password == '': new_password = old_password
#     new_user = User(id = request.user.id if is_prole else request.POST.get('selected_user'),\
#                     username = new_username if new_username else request.user.username,\
#                     password = new_password,\
#                     email = new_email if new_email else request.user.email,\
#                     first_name = new_first_name if new_first_name else request.user.first_name,\
#                     last_name = new_last_name if new_last_name else request.user.last_name)
#     #Changes existing user. You'll need to define a new function to create new ones.
#     #It creates a user object, if a category is empty, then it takes the old one
#     new_user.save()
#     return render(request, 'user_management.html')
#     #Requires page: USER_MANAGEMENT.HTML

# def user_select(request): 
#     #Helper for the user_management.
#     #3 search criteria, at most 1 permissable
#     #Filters are name, user_id and email.
#     #params are the parameters of search
#     #For example, if filters = 'name' and params = 'rick', you search for users whose name is rick.
#     if not_auth := gatekeeper(request, True): return not_auth
#     filters, params = map(request.POST.get,['filters', 'params'])
#     if sum(bool(screen for screen in filters)) > 1: return {'TooManyRequests': True, 'Error': True}
#     match filters:
#         case 'name': return User.objects.filter(name = params)
#         case 'user_id': return User.objects.filter(id = params)
#         case 'email': return User.objects.filter(email = params)
#     #This needs no html templates.

# def receive_pellet(request):
#     #Function to manage fetching a pellet.
#     if not_auth := gatekeeper(request): return not_auth
#     if request.method != 'POST':
#          #Fetching current pellets
#          #The __str__(self) is called by str(pellet).
#          pellet = Pellet.objects.filter(is_inbound = True).order_by('-inbound_shipment')
#          return render(request, 'receive_package.html', {'received_pellets': pellet, 'string_rep_of_pellet': str(pellet)}) 
#     column, row, pellet_name, pellet_desc = map(request.POST.get, ['column', 'row', 'name', 'description'])
#     new_received_pellet = Pellet(is_inbound = True, column = column, row = row, pellet_name = pellet_name, pellet_desc = pellet_desc)
#     try:
#         new_received_pellet.save()
#         return render(request, 'receive_package.html', {'success': True}, status = 409)
#     except IntegrityError as IE:
#         #Happens when one tries to save a pellet where there is already one
#         #Information that is NOT positional is passed back in context.
#         return render(request, 'receive_package.html', {'SpaceAlreadyOccupied': True, 'name': pellet_name, 'desc': pellet_desc})
#     #REQUIRES TEMPLATE: RECEIVE_PACKAGE.HTML

# def build_order(request):
#     #Builds an order
#     #Use GET to first fetch template, then submit form with POST
#     if not_auth := gatekeeper(request): return not_auth
#     if request.method == 'GET': return render(request, 'build_an_order.html', {'orders': Order.objects.all()})
#     due_date, order_type, quantity, destination, title, description = map(request.POST.get, ['due_date', 'type', 'quantity', 'destination', 'title', 'description'])
#     order = Order(due_date = due_date, order_type = order_type, quantity = quantity, destination = destination, title = title, description = description)
#     order.save()
#     return render(request, 'build_an_order.html', {'Order': order})
#     #REQUIRES TEMPLATE: BUILD_AN_ORDER.HTML


# def build_a_shipment(request):
#     #Building a new shipment
#     #Access with GET method to fetch upcoming shipments
#     #Access with POST method to build a new shipment
#     #One and only one shipment per day
#     #On success creation, return a list of overdue and recent (within 14 days of shipment) orders with respect to the shipment
#     if not_auth := gatekeeper(request): return not_auth
#     if request.method == 'GET': return render(request, 'build_a_shipment.html', {'shipments': Outbound.objects.all()})
#     shipment_date, desc, dest = map(request.POST.get, ['date', 'desc', 'dest'])
#     new_shipment_outbound = Outbound(shipment_date = shipment_date, desc = desc, dest = dest)
#     try:
#         new_shipment_outbound.save()
#         return render(request, 'build_a_shipment.html', {'shipment_id': new_shipment_outbound.id, 'shipment_str': str(new_shipment_outbound), 'overdue_shipments': Order.objects.filter(date__lt = shipment_date), 'close_to_due': Order.objects.filter(date__range = [start := datetime.strptime(shipment_date, '%Y-%m-%d').date(), start + timedelta(days = 14)])})
#     except IntegrityError as IE:
#         return render(request, 'build_a_shipment.html', {'ShipmentAlreadyExists': True})
#     #REQUIRES TEMPLATE: BUILD_A_SHIPMENT.HTML
# # Create your views here.
