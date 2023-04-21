from django.urls import include, path
from rest_framework import routers
from .views import *
from . import models


router = routers.DefaultRouter()
router.register('users', Userviewset)
router.register('cargo', CargoViewset)
router.register('order', OrderViewset)
router.register('products', ProductsViewset)
router.register('pellet', PelletViewset)

urlpatterns = [
    path('', home, name='index'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]