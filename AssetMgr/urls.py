from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('', views.home, name='index'),
     path('', include(routers.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]