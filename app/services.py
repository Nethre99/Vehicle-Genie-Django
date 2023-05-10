import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from django_pandas.io import read_frame
from django.db.models import F
import pandas as panda
from sklearn.metrics import accuracy_score, f1_score

from .serializers import VehicleSerializer
from . import models


def getMergedDf():
    userVehicle = models.UserVehicle.objects.all()
    vehicleQS = models.vehicles.objects.all()

    uvDf = read_frame(userVehicle)
    vDf = read_frame(vehicleQS)
    vDf = vDf.rename(columns={'vehicle_Id': 'Vehicle_Id'})

    # Join the dataframes on Vehicle_Id column
    joined_df = panda.merge(uvDf, vDf, how='inner', on='Vehicle_Id')

    return joined_df


def getCreatedPivotForUserVehicleHistory():
    try:
        joined_df = getMergedDf()

        selected_df = joined_df.loc[:, ~joined_df.columns.duplicated()]
        uvUpdatedDF = selected_df.loc[:,
                      ['Client_Id', 'Vehicle_Id', 'brand', 'model', 'transmission', 'body', 'year', 'fuel', 'location']]

        print("get Created Pivot For User Vehicle History | Selected DataFrame: \n", uvUpdatedDF)

        pivot_table = panda.pivot_table(selected_df, values='Vehicle_Id', index=['Client_Id'],
                                        columns=['brand', 'model', 'transmission', 'body', 'year', 'fuel', 'location'],
                                        aggfunc='count', fill_value=0)

        print("get Created Pivot For User Vehicle History | pivot_table: \n", pivot_table)

        return pivot_table
    except Exception as e:
        print("Error occurred while create User Vehicle Matrix:", str(e))
        return None



def getSimilarVehicles(vehicleFeature):
    try:
        print("Get Similar Vehicles: ", vehicleFeature)
        similar_vehicles_1 = models.vehicles.objects.filter(
            brand=vehicleFeature[0],
            model=vehicleFeature[1],
            transmission=vehicleFeature[2]
        )
        print("Get Similar Vehicles 1: ", similar_vehicles_1)

        # check for vehicles matching brand, body, and transmission
        similar_vehicles_2 = models.vehicles.objects.filter(
            brand=vehicleFeature[0],
            body=vehicleFeature[3],
            transmission=vehicleFeature[2]
        )
        print("Get Similar Vehicles 2: ", similar_vehicles_2)

        # check for vehicles matching body, transmission, fuel, and year
        similar_vehicles_3 = models.vehicles.objects.filter(
            body=vehicleFeature[3],
            transmission=vehicleFeature[2],
            fuel=vehicleFeature[5],
            year=vehicleFeature[4]
        )
        print("Get Similar Vehicles 3: ", similar_vehicles_3)

        similar_vehicles = list(set(list(similar_vehicles_1) + list(similar_vehicles_2) + list(similar_vehicles_3)))
        print("Get Similar Vehicles: ", similar_vehicles)
        return similar_vehicles
    except Exception as e:
        print("Error occurred while retrieving Similar Vehicles:", str(e))
        return None

def getRecommendations(clientId):
    try:
        uv_matrix = getCreatedPivotForUserVehicleHistory()
        print("Get Recommendations | uv matrix: \n", uv_matrix)

        vehiclePreferences = uv_matrix.loc[clientId]
        print("Get Recommendations | vehicle preferences: ",vehiclePreferences)
        recommendedVehicles = set()

        for feature in vehiclePreferences.index:
            # print("Get Recommendations | ForLoop vehicle preferences:\n", feature)
            if vehiclePreferences[feature] > 0:
                print("Get Recommendations | If Statement vehicle preferences:\n", vehiclePreferences[feature])
                similar_vehicles = getSimilarVehicles(feature)
                if similar_vehicles is not None:
                    for similar_vehicle in similar_vehicles:
                        recommendedVehicles.add(similar_vehicle.vehicle_Id)

        recommendedVehicles -= set(vehiclePreferences[vehiclePreferences == 1].index)
        recommendedVehicles = list(recommendedVehicles)[:20]

        return recommendedVehicles
    except Exception as e:
        print("Error occurred while retrieving Recommendations:", str(e))
        return None


def getRecommendedVehicleList(clientId):
    try:
        vehicleIdList = getRecommendations(clientId)
        vehiclesModels = models.vehicles.objects.filter(vehicle_Id__in=vehicleIdList)
        serializedVehicleList = VehicleSerializer(vehiclesModels, many=True)
        return serializedVehicleList.data
    except Exception as e:
        print("Error occurred while retrieving Recommended Vehicle List:", str(e))
        return None

