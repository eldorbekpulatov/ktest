from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import serializers
from ad.models import *

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)
        read_only = ('key')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name',)
        read_only = ('id', 'name')

class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = ('id', 'name','file','dvm','osc','rctrl','actrl','eload')
        read_only = ('id', 'name','file','dvm','osc','rctrl','actrl','eload')

class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = ('id', 'name', 'type', 'serialNumber', 'kepcoNumber', 'calibrationDate', 'expirationDate', 'resourceID')
        read_only = ('id', 'name', 'type', 'serialNumber', 'kepcoNumber', 'calibrationDate', 'expirationDate', 'resourceID')

class StationSerializer(serializers.ModelSerializer):
    instrument_set = InstrumentSerializer(many=True)
    products= ProductSerializer(many=True)
    class Meta:
        model = Station
        read_only = ('id', 'name','instrument_set', 'products')
        fields = ('id', 'name','instrument_set', 'products')

class ModelSerializer(serializers.ModelSerializer):
    scripts = ScriptSerializer(many=True)
    class Meta:
        model = Model
        fields = ('id', 'name', 'voltage', 'current', 'scripts')
        read_only = ('id', 'name', 'voltage', 'current', 'scripts')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name', 'email',]
        read_only = ['id', 'username', 'last_name', 'first_name', 'email', ]

class CardSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    station = StationSerializer(many=False)
    product = ProductSerializer(many=False)
    model = ModelSerializer(many=False)
    class Meta:
        model = Card
        fields = ('id', 'serial', 'user', 'station', 'product', 'model',)
        read_only = ('id', 'serial', 'user', 'station', 'product', 'model',)


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ('id', 'file', 'script', 'status', 'card' )
        read_only = ('id', 'file', 'script', 'status', 'card')

