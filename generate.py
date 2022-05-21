import random
import pandas as pd
from scipy import spatial
import numpy as np
import operator

anime_csv = pd.read_csv("anime.csv")

def anime_formatter():
    anime_dictionary = []

    for index, anime in anime_csv.iterrows():
        try:
            anime_dictionary.append([anime[0], [int(i) for i in anime[6].split(",")]])
        except:
            pass
        
    return anime_dictionary

def get_distance(genre_1, genre_2):
    genre_similarity = spatial.distance.cosine(genre_1, genre_2)
    return genre_similarity
anime_dictionary = anime_formatter()
def get_nearest_neighbors(genre_list: list, K: int):
    distances = []
    for anime in anime_dictionary:
        dist = get_distance(genre_list, anime[1]) 
        distances.append((anime[0], dist))

    distances.sort(key=operator.itemgetter(1)) # Sort the distances of animes
    neighbors = []
    for i in range(K):
        neighbors.append(distances[i][0])
    return neighbors

with open("ratings.csv", "w+") as file: 
    file.write("user_id,anime_id,rating\n")
    for index, anime in anime_csv.iterrows():
        users = []
        for user in range(10):
            user_id = random.randint(1,49)
            while user_id in users:
                user_id = random.randint(1,49)
            users.append(user_id)
            value = random.randint(5,10)
            file.write(f"{user_id}, {anime[0]}, {value}\n")
 