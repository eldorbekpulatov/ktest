from rest_framework import serializers
from django.contrib.auth.models import User
from ad.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name', 'email']
        read_only = ['id', 'username', 'last_name', 'first_name', 'email']

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
    instruments = InstrumentSerializer(many=True)
    class Meta:
        model = Station
        read_only = ('id', 'name','instruments')
        fields = ('id', 'name','instruments')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name',)
        read_only = ('id', 'name')

class ModelSerializer(serializers.ModelSerializer):
    scripts = ScriptSerializer(many=True)
    class Meta:
        model = Model
        fields = ('id', 'name', 'voltage', 'current', 'scripts')
        read_only = ('id', 'name', 'voltage', 'current', 'scripts')







