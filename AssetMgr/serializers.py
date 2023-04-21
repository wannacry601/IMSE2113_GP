from django.contrib.auth.models import User, Group
from rest_framework import serializers 
from .models import *

class PelletSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Pellet
        fields = '__all__'

    def create(self, validated_data):
        return Pellet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.is_inbound = validated_data.get('is_inbound', instance.is_inbound)
        instance.column = validated_data.get('column', instance.column)
        instance.row = validated_data.get('row', instance.row)
        instance.pellet_name = validated_data.get('pellet_name', instance.pellet_name)
        instance.pellet_desc = validated_data.get('pellet_desc', instance.pellet_desc)
        instance.source = validated_data.get('source', instance.source)
        instance.destination = validated_data.get('destination', instance.destination)
        instance.save()
        return instance


class CargoSerializer(serializers.HyperlinkedModelSerializer):
    on_pellet = serializers.PrimaryKeyRelatedField(queryset=Pellet.objects.all(), required=False, allow_null=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Cargo
        fields = '__all__'

    def create(self, validated_data):
        return Cargo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.on_pellet = validated_data.get('on_pellet', instance.on_pellet)
        instance.destination = validated_data.get('destination', instance.destination)
        instance.arrival_date = validated_data.get('arrival_date', instance.arrival_date)
        instance.origin = validated_data.get('origin', instance.origin)
        instance.due_outbound_date = validated_data.get('due_outbound_date', instance.due_outbound_date)
        instance.name = validated_data.get('name', instance.name)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    order_type = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all())

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.order_type = validated_data.get('order_type', instance.order_type)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.destination = validated_data.get('destination', instance.destination)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class ProductsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

    def create(self, validated_data):
        return Products.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'groups', 'first_name', 'last_name', 'is_staff']
    def update(self, instance, data):
        instance.email = data.get('email', instance.email)
        instance.username = data.get('username', instance.username)
        instance.id = data.get('id', instance.id)
        instance.first_name = data.get('first_name', instance.first_name)
        instance.last_name = data.get('first_name', instance.first_name )

