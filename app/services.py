from typing import List, Any
from sklearn.metrics.pairwise import cosine_similarity

from . import serializers
from . import models


def getAllVehicles():
    vehicleList = models.vehicles.objects.all()
    serialize = serializers.VehicleSerializer(vehicleList, many=True)
    return serialize.data


def createUserVehicleMatrix():
    # userVehicle_queryset = models.UserVehicle.objects.filter(Client_Id=Id)
    userVehicle_queryset = models.UserVehicle.objects.all()

    matrix: list[list[Any]] = []
    # matrix = []

    for user_vehicle in userVehicle_queryset:
        data_collection = [user_vehicle.Client_Id, user_vehicle.Vehicle_Id]
        matrix.append(data_collection)

    print(matrix)
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


# def getRecommendedVehicleList(Id):
#     global similar_vehiclePreferences
#
#     similarUsers = getSimilarUsers(Id)
#     userVehicleMatrix = createUserVehicleMatrix()
#
#     vehiclePreferences = None
#     for user_vehicle in userVehicleMatrix:
#         if user_vehicle[0] == Id:
#             vehiclePreferences = user_vehicle
#             break
#
#     if vehiclePreferences is None:
#         # Handle the case when Id is not found in the matrix
#         raise ValueError(f"User with Id {Id} not found in the userVehicleMatrix.")
#
#     recommendedVehicles = set()
#     similar_vehiclePreferences = []
#
#     for client in similarUsers:
#         for user_vehicle in userVehicleMatrix:
#             if user_vehicle[0] == client:
#                 similar_vehiclePreferences = user_vehicle
#                 break
#
#         recommendedVehicles.update(set(similar_vehiclePreferences[0]))
#
#     recommendedVehicles -= set(vehiclePreferences[2])
#
#     return recommendedVehicles
