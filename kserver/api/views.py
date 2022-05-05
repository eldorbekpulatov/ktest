from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from ad.models import *
from api.serializers import *
from django.shortcuts import get_object_or_404


class GetAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        userSerializer = UserSerializer(user, many=False)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'user': userSerializer.data, 'token': token.key}, status=status.HTTP_200_OK)
    

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
        return Response(data, status=status.HTTP_200_OK)


class ProductsAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        station = get_object_or_404(Station, id=request.data["id"])
        stationSerializer = StationSerializer(station, many=False)
        products = station.products.all()
        productSerializer = ProductSerializer(products, many=True)
        data = {    'station': stationSerializer.data,
                    'products':productSerializer.data   }
        return Response(data, status=status.HTTP_200_OK)


class ModelsAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        product = get_object_or_404(Product, id=request.data["id"])
        productSerializer = ProductSerializer(product, many=False)
        models = product.model_set.all()
        modelSerializer = ModelSerializer(models, many=True)
        data = {'product': productSerializer.data, 'models':modelSerializer.data}
        return Response(data, status=status.HTTP_200_OK)


class ScriptsAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        model = get_object_or_404(Model, id=request.data["id"])
        modelSerializer = ModelSerializer(model, many=False)
        data = {'model': modelSerializer.data}
        return Response(data, status=status.HTTP_200_OK)


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
            'model': modelSerializer.data,
        }
        return Response(data, status=status.HTTP_200_OK)


class CardAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        querySet = Card.objects.filter(serial=request.data['serial_number'])
        if querySet.exists():
            cardObject = querySet[0]
            cardSerializer = CardSerializer(cardObject, many=False)
            if cardObject.model.id == int(request.data["model_id"]) and cardObject.product.id == int(request.data["product_id"]):
                return Response(cardSerializer.data, status=status.HTTP_202_ACCEPTED) 
            else:
                return Response(cardSerializer.data, status=status.HTTP_226_IM_USED)
        else:
            return Response(querySet, status=status.HTTP_204_NO_CONTENT)
        

    def post(self, request, format=None):
        card, new_card = Card.objects.get_or_create(serial=request.data['serial_number'])
        try:
            card.station = get_object_or_404(Station, id=request.data["station_id"])
            card.product = get_object_or_404(Product, id=request.data["product_id"])
            card.model = get_object_or_404(Model, id=request.data["model_id"])
            card.user = request.user
            card.save()

            for key,file in request.FILES.items():
                [script_id, log_status] = key.split("-")
                
                script = get_object_or_404(Script, id=script_id)
                log, new_log = Log.objects.get_or_create(card=card, script=script)
                if new_log:
                    log.file.save("_".join([card.serial,script.name]), file, save=True)
                else:
                    with open(log.file.path, "ab") as old_file:
                        old_file.write(file.read())
                log.status = log_status
                log.save()         
            return Response("Successfully updated the database.", status=status.HTTP_201_CREATED)                  
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

