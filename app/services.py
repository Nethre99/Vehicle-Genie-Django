from typing import List, Any
import pandas as panda
from sklearn.metrics.pairwise import cosine_similarity
from django_pandas.io import read_frame

from . import serializers
from . import models


def getAllVehicles():
    vehicleList = models.vehicles.objects.all()
    serialize = serializers.VehicleSerializer(vehicleList, many=True)
    return serialize.data


def createUserVehicleMatrix():
    # userVehicle_queryset = models.UserVehicle.objects.filter(Client_Id=Id)
    userVehicle_queryset = models.UserVehicle.objects.all()

    # read query set as a dataframe
    dataframe = read_frame(userVehicle_queryset)

    matrix = dataframe.groupby(['Client_Id', 'Vehicle_Id']).size().unstack(fill_value=0)

    return matrix


def calculateCosineSimilarity(userVehicleMatrix):
    cosineSim = cosine_similarity(userVehicleMatrix)
    print(cosineSim)
    return cosineSim


def getSimilarUsers(Id):
    userVehicleMatrix = createUserVehicleMatrix()
    cosineSimilarity = calculateCosineSimilarity(userVehicleMatrix)

    user_sim = cosineSimilarity[Id]
    similar_users = user_sim.argsort()[::-1][1:5 + 1]

    return similar_users


def getRecommendedVehicleList(Id):
    global similar_vehiclePreferences

    similarUsers = getSimilarUsers(Id)
    vehiclePreferences = createUserVehicleMatrix().loc[Id]

    recommendedVehicles = set()

    for client in similarUsers:
        similar_vehiclePreferences = createUserVehicleMatrix().loc[client]

    recommendedVehicles.update(similar_vehiclePreferences[similar_vehiclePreferences == 1].index)
    recommendedVehicles -= set(vehiclePreferences[vehiclePreferences == 1].index)

    return recommendedVehicles
