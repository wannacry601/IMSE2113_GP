from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('how/', views.how, name='how'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'), 
    path('disable/', views.disable, name='disable'),
    path('changeUser/', views.changeUser, name='changeUser'),
    path('addUser/', views.addUser, name='addUser'),

]