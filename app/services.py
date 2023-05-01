from sklearn.metrics.pairwise import cosine_similarity
from django_pandas.io import read_frame

from . import serializers
from . import models


def getAllVehicles():
    try:
        vehicleList = models.vehicles.objects.all()
        print("Get All vehicles: ", vehicleList)
        serialize = serializers.VehicleSerializer(vehicleList, many=True)
        print("Get serialized All vehicles: ", serialize.data)
        return serialize.data
    except Exception as e:
        print("Error occurred while retrieving all vehicles: ", str(e))
        return None

def createUserVehicleMatrix():
    try:
        # userVehicle_queryset = models.UserVehicle.objects.filter(Client_Id=Id)
        userVehicle_queryset = models.UserVehicle.objects.all()
        # read query set as a dataframe
        dataframe = read_frame(userVehicle_queryset)
        matrix = dataframe.groupby(['Client_Id', 'Vehicle_Id']).size().unstack(fill_value=0)
        print("Create User Vehicle Matrix: \n", matrix)
        return matrix
    except Exception as e:
        print("Error occurred while create User Vehicle Matrix:", str(e))
        return None


def calculateCosineSimilarity():
    userVehicleMatrix = createUserVehicleMatrix()
    try:
        cosineSim = cosine_similarity(userVehicleMatrix)
        print("calculate Cosine Similarity: ",cosineSim)
        return cosineSim
    except Exception as e:
        print("Error occurred while calculate Cosine Similarity:", str(e))
        return None


def getSimilarUsers(Id):
    try:
        matrix = createUserVehicleMatrix()
        cosineSimilarity = calculateCosineSimilarity()

        row_index = matrix.index.get_loc(Id)
        print("Row Index: ",row_index)
        user_sim = cosineSimilarity[row_index]
        # if user_sim in None: return []

        print("Get Similar Users cosine User similarity: ", user_sim)
        similar_users = user_sim.argsort()[::-1][1:5 + 1]
        print("Get similar users: ", similar_users)
        return similar_users
    except IndexError as indexError:
        print("Index Out of bound in get similar users: ", str(indexError))
    except Exception as e:
        print("Error occurred while retrieving get Similar Users:", str(e))
        return None


def getRecommendations(Id):
    try:
        global similar_vehiclePreferences
        uv_matrix = createUserVehicleMatrix()
        similarUsers = getSimilarUsers(Id)
        vehiclePreferences = uv_matrix.loc[Id]

        print("Get Recommendations similar users: ", similarUsers)
        print("Get Recommendations vehicle preferences: ", vehiclePreferences)

        recommendedVehicles = set()
        print('recommendedVehicles', recommendedVehicles)
        vehPreferences = []

        for client in similarUsers:
            if client in uv_matrix.index:
                print("Get Recommendations clients in Similar Users: ", client)
                similar_vehiclePreferences = uv_matrix.loc[client]
                print("Similar vehicle preferences: ", similar_vehiclePreferences)
                vehPreferences.append(similar_vehiclePreferences)
            else:
                print("Get Recommendations clients None: ", client)

        print("Vehicle Preferences List: ", vehPreferences)
        recommendedVehicles.update(similar_vehiclePreferences[similar_vehiclePreferences == 1].index)
        recommendedVehicles -= set(vehiclePreferences[vehiclePreferences == 1].index)
        print("Recommendation Id List: ", recommendedVehicles)

        return recommendedVehicles
    except Exception as e:
        print("Error occurred while retrieving get Recommendations:", str(e))
        return None


def getRecommendedVehicleList(Id):
    try:
        vehicleIdList = getRecommendations(Id)
        print("Get Recommended Vehicle Id List: ", vehicleIdList)
        vehicles = models.vehicles.objects.filter(vehicle_Id__in=vehicleIdList)

        print("Get Recommended Vehicle Id List: ", vehicles)

        try:
            serializedVehicleList = serializers.VehicleSerializer(vehicles, many=True)
            return serializedVehicleList.data
        except Exception as e:
            print("Error occurred while serializing vehicle data:", str(e))

    except Exception as e:
        print("Error occurred while retrieving get Recommended Vehicle List:", str(e))
        return None


# def calculateAccuracy(recommendationList, id):
#     try:
#         vehicleIds = models.UserVehicle.objects.filter(client_Id=id).values_list("vehicle_Id", flat=True)
#         filtered_vehicle_list = [vehicle for vehicle in getAllVehicles() if vehicle['vehicle_Id'] in vehicleIds]
#
#         # Convert into tuples to set the intersection
#         recommendation_tuple = [tuple(recommendationList) for recommendation in recommendationList]
#         watchedVehicle_tuple = [tuple(filtered_vehicle_list) for vehicles in filtered_vehicle_list]
#
#         recommendation_set = set(recommendation_tuple)
#         vehicleList_set = set(watchedVehicle_tuple)
#         intersection = recommendation_set.intersection(vehicleList_set)
#
#         print("Recommended vehicles:", recommendationList)
#         print("User watched vehicles:", filtered_vehicle_list)
#         print("Intersection:", intersection)
#
#         accuracy = len(intersection)/len(recommendationList)
#         print("Accuracy: ", accuracy)
#         return accuracy
#     except Exception as e:
#         print("Error occurred while retrieving calculate Accuracy:", str(e))
#         return None
#
