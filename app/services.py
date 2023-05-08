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


# def testSet(id):
#
#
#
# def getRecommendedVehicleList(Id):
#     try:
#         vehicleIdList = getRecommendations(Id)
#         print("Get Recommended Vehicle Id List: ", vehicleIdList)
#         vehicles = models.vehicles.objects.filter(vehicle_Id__in=vehicleIdList)
#         print("Get Recommended Vehicle Id List: ", vehicles)
#
#         serializedVehicleList = VehicleSerializer(vehicles, many=True)
#         recommended_vehicle_list = serializedVehicleList.data
#
#         # Get the actual vehicle list from the test set
#         actual_vehicle_list = test_set[test_set['Client_Id'] == Id]['Vehicle_Id'].tolist()
#
#         # Compute accuracy and f1-score
#         accuracy = accuracy_score(actual_vehicle_list, recommended_vehicle_list)
#         f1 = f1_score(actual_vehicle_list, recommended_vehicle_list, average='weighted')
#
#         return recommended_vehicle_list, accuracy, f1
#     except Exception as e:
#         print("Error occurred while retrieving get Recommended Vehicle List:", str(e))
#         return None





# def recommend_vehicle(client_id):
#     # try:
#     user_vehicle_matrix = getCreatedPivotForUserVehicleHistory()
#
#     user_history = user_vehicle_matrix.loc[client_id]
#     user_history = np.array(user_history).reshape(1, -1)
#
#     vehicle_similarity = cosine_similarity(user_vehicle_matrix, user_history)
#     vehicle_similarity = vehicle_similarity.flatten()
#
#     top_10_vehicles = np.argsort(vehicle_similarity)[::-1][:10]
#     top_10_vehicle_similarity = vehicle_similarity[top_10_vehicles]
#
#     top_10_vehicle_details = models.vehicles.objects.filter(vehicle_Id__in=user_vehicle_matrix.columns[top_10_vehicles])
#
#     # top_10_vehicle_details = models.vehicles.objects.filter(vehicle_Id__in=user_vehicle_matrix.columns[top_10_vehicles])
#
#     top_10_vehicle_scores = []
#     for vehicle in top_10_vehicle_details:
#         vehicle_scores = user_history * np.array(vehicle.get_features())
#         vehicle_scores = vehicle_scores[0][np.where(vehicle_scores[0] > 0)]
#         if len(vehicle_scores) > 0:
#             mean_score = np.mean(vehicle_scores)
#         else:
#             mean_score = 0
#         top_10_vehicle_scores.append(mean_score)
#
#     top_10_vehicle_scores = np.array(top_10_vehicle_scores)
#     top_10_vehicle_scores /= np.max(top_10_vehicle_scores)
#     top_10_vehicle_scores *= 5
#     top_10_vehicle_scores = np.round(top_10_vehicle_scores, 2)
#
#     vehicle_scores_df = panda.DataFrame({'Vehicle_Id': user_vehicle_matrix.columns[top_10_vehicles],
#                                          'Similarity_Score': top_10_vehicle_similarity,
#                                          'Score': top_10_vehicle_scores})
#
#     vehicle_scores_df = vehicle_scores_df.sort_values(by=['Score', 'Similarity_Score'], ascending=False)
#
#     serializer = VehicleSerializer(top_10_vehicle_details, many=True)
#
#     return serializer.data
# except Exception as e:
#     print("Error occurred while recommending vehicle:", str(e))
#     return None

# def getRecommendations(userId):
#     try:
#         pivot = getCreatedPivotForUserVehicleHistory()
#
#         userBrowsingHistory = pivot.loc[userId]
#         print("Get Recommendations | user Browsing history:\n", userBrowsingHistory)
#
#         userSimilarityScore = cosine_similarity([userBrowsingHistory], pivot)[0]
#         print("Get Recommendations | user Similarity Score(Cosine_Sim):\n", userSimilarityScore)
#
#         userSimScoreDF = panda.DataFrame({'client_Id': pivot.index, 'Similarity_Score': userSimilarityScore})
#         print("Get Recommendations | Similarity Score DF:\n", userSimScoreDF)
#
#         topSimilarUsers = userSimScoreDF.sort_values('Similarity_Score', ascending=False).head() #[userId] removed
#         print("Get Recommendations | Top Most Similar users:\n", topSimilarUsers)
#
#         similarVehicles = panda.DataFrame(columns=['vehicle_Id, Similarity_Score'])
#         for user in topSimilarUsers['client_Id']:
#             print("Get Recommendations | For Loop user: ", user)
#             if user != userId:
#                 print("Get Recommendations | Check the Users: ", user)
#
#                 pivot2D =
#
#                 similarity_score = cosine_similarity([pivot.loc[user]], [userBrowsingHistory][0][0])
#                 # similarity_score = cosine_similarity([pivot.loc[user]], np.array([userBrowsingHistory][0][0]).reshape(1, -1))
#                 print("Get Recommendations | Similaity Score count:\n", similarity_score)
#
#                 similarVehicles = similarVehicles._append(
#                     panda.DataFrame(
#                         {
#                             'vehicle_Id': pivot.loc[user][pivot.loc[user] > 0].index.tolist(),
#                             'similarity_score': [similarity_score] * len(pivot.loc[user][pivot.loc[user] > 0].index)
#                         },
#                         ignore_index=True
#                     )
#                 )
#                 print("Get Recommendations | Similar Vehicles:\n", similarVehicles)
#
#         vehicleScore = similarVehicles.groupby('vehicle_Id')['Similarity_score'].mean().sort_values(ascending=True)
#         print("Get Recommendations | Vehicle Score:\n", vehicleScore)
#
#         topMostVehicles = vehicleScore.head().index.toList()
#
#         top_10_vehicle_details = models.vehicles.objects.filter(vehicle_Id__in = topMostVehicles)
#
#         serializer = VehicleSerializer(top_10_vehicle_details, many=True)
#
#         return serializer.data
#
#     except Exception as e:
#         print("Error occurred while recommending vehicle:")
#         print("Type: ", type(e).__name__)
#         print("Message: ", str(e))
#         return None


# def calculateCosineSimilarity():
#     userVehicleMatrix = createUserVehicleMatrix()
#     try:
#         cosineSim = cosine_similarity(userVehicleMatrix)
#         print("calculate Cosine Similarity: ",cosineSim)
#         return cosineSim
#     except Exception as e:
#         print("Error occurred while calculate Cosine Similarity:", str(e))
#         return None
#
#
# def getSimilarUsers(Id):
#     try:
#         matrix = createUserVehicleMatrix()
#         cosineSimilarity = calculateCosineSimilarity()
#
#         row_index = matrix.index.get_loc(Id)
#         print("Row Index: ", row_index)
#         user_sim = cosineSimilarity[row_index]
#
#         print("Get Similar Users cosine User similarity: ", user_sim)
#         similar_users = user_sim.argsort()[::-1][1:5 + 1]
#         print("Get similar users: ", similar_users)
#         return similar_users
#     except IndexError as indexError:
#         print("Index Out of bound in get similar users: ", str(indexError))
#     except Exception as e:
#         print("Error occurred while retrieving get Similar Users:", str(e))
#         return None
#
#
# def getRecommendations(Id):
#     try:
#         global similar_vehiclePreferences
#         uv_matrix = createUserVehicleMatrix()
#         similarUsers = getSimilarUsers(Id)
#         vehiclePreferences = uv_matrix.loc[Id]
#
#         print("Get Recommendations similar users: ", similarUsers)
#         print("Get Recommendations vehicle preferences: ", vehiclePreferences)
#
#         recommendedVehicles = set()
#         print('recommendedVehicles', recommendedVehicles)
#         vehPreferences = []
#
#         for client in similarUsers:
#             print("Get Recommendations clients in Similar Users for loop: ", client)
#             if client in uv_matrix.index:
#                 similar_vehiclePreferences = uv_matrix.loc[client]
#                 print("Similar vehicle preferences: ", similar_vehiclePreferences)
#             else:
#                 print("Get Recommendations clients None: ", client)
#
#         print("Vehicle Preferences List: ", vehPreferences)
#         recommendedVehicles.update(similar_vehiclePreferences[similar_vehiclePreferences == 1].index)
#         recommendedVehicles -= set(vehiclePreferences[vehiclePreferences == 1].index)
#         print("Recommendation Id List: ", recommendedVehicles)
#
#         return recommendedVehicles
#     except Exception as e:
#         print("Error occurred while retrieving get Recommendations:", str(e))
#         return None
#
#
# def getRecommendedVehicleList(Id):
#     try:
#         vehicleIdList = getRecommendations(Id)
#         print("Get Recommended Vehicle Id List: ", vehicleIdList)
#         vehicles = models.vehicles.objects.filter(vehicle_Id__in=vehicleIdList)
#         print("Get Recommended Vehicle Id List: ", vehicles)
#
#         serializedVehicleList = VehicleSerializer(vehicles, many=True)
#         return serializedVehicleList.data
#     except Exception as e:
#         print("Error occurred while retrieving get Recommended Vehicle List:", str(e))
#         return None
