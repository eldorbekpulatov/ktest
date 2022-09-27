from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.shortcuts import get_object_or_404
from .serializers import *
from .token import *
from ad.models import *


class GetAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    
class StationsAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        stations = list(user.station_set.all())
        for group in user.groups.all():
            for station in group.station_set.all():
                if not station in stations:
                    stations.append(station)
        userSerializer = UserSerializer(user, many=False)
        stationSerializer = StationSerializer(stations, many=True)
        data = {'user': userSerializer.data, 'stations':stationSerializer.data}
        return Response(data)

class ProductsAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        station = get_object_or_404(Station, id=request.data["id"])
        products = station.products.all()
        stationSerializer = StationSerializer(station, many=False)
        productSerializer = ProductSerializer(products, many=True)
        data = {'station': stationSerializer.data, 'products':productSerializer.data}
        return Response(data)

class ModelsAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        product = get_object_or_404(Product, id=request.data["id"])
        models = product.model_set.all()
        productSerializer = ProductSerializer(product, many=False)
        modelSerializer = ModelSerializer(models, many=True)
        data = {'product': productSerializer.data, 'models':modelSerializer.data}
        return Response(data)

class ScriptsAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        model = get_object_or_404(Model, id=request.data["id"])
        modelSerializer = ModelSerializer(model, many=False)
        data = {'model': modelSerializer.data}
        return Response(data)

class ReloadAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        station = get_object_or_404(Station, id=request.data["station_id"])
        stationSerializer = StationSerializer(station, many=False)
        product = get_object_or_404(Product, id=request.data["product_id"])
        productSerializer = ProductSerializer(product, many=False)
        model = get_object_or_404(Model, id=request.data["model_id"])
        modelSerializer = ModelSerializer(model, many=False)

        data = {
            'station': stationSerializer.data, 
            'product': productSerializer.data,
            'model': modelSerializer.data
        }
        return Response(data)

class CardAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        station = get_object_or_404(Station, id=request.data["station_id"])
        product = get_object_or_404(Product, id=request.data["product_id"])
        model = get_object_or_404(Model, id=request.data["model_id"])
        log = request.data['log_file']
        print(type(log))

        data = {
            'station': "station", 
            'product': "product",
            'model': "model",
            'log':"log"
        }
        return Response(data)