from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import serializers
from . import models
from . import services


# Create your views here.
@api_view(['GET', 'POST'])
def index(request):
    color = {
        'name': 'black'
    }

    return Response(color)


@api_view(['GET'])
def getAllVehicles(request):
    vehicleList = models.vehicles.objects.all()
    serialize = serializers.VehicleSerializer(vehicleList, many=True)
    return Response(serialize.data)


@api_view(['GET'])
def getById(request, pk):
    vehicle = models.vehicles.objects.get(vehicle_Id=pk)
    serialize = serializers.VehicleSerializer(vehicle, many=False)
    return Response(serialize.data)


@api_view(['POST'])
def addVehicle(request):
    serialize = serializers.VehicleSerializer(data=request.data)

    if serialize.is_valid():
        serialize.save()

    return Response(serialize.data)


"""    User Vehicle data     """

@api_view(['GET'])
def getUserVehicles(request):
    UserVehicleList = models.UserVehicle.objects.all()
    serialize = serializers.UserVehicleSerializer(UserVehicleList, many=True)
    return Response(serialize.data)


""" Implementation"""

@api_view(['GET'])
def getRecommendations(request, UserId):
    UserID= {
        "UserId": UserId
    }
    id = UserID.get("UserId")
    recommendations = services.getRecommendedVehicleList(id)
    return Response(recommendations)