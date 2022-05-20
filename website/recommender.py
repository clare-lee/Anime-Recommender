import json
import pandas as pd
import operator
from scipy import spatial
from .models import Anime
from sqlalchemy.sql import func

def anime_formatter():
    animelist = Anime.query.all()
    # .with_entities(func.avg(Anime.ratings.rating))
    anime_dictionary = []
    print(animelist[0])

    for anime in animelist:
        anime_dictionary.append([anime.name, [int(i) for i in anime.binary_genres.split(",")]])
    return anime_dictionary

def get_distance(genre_1, genre_2):
    genre_similarity = spatial.distance.cosine(genre_1, genre_2)
    return genre_similarity

def get_nearest_neighbors(genre_list: list, K: int):
    distances = []
    anime_dictionary = anime_formatter()
    
    for anime in anime_dictionary:
        dist = get_distance(genre_list, anime[1]) 
        distances.append((anime[0], dist))

    distances.sort(key=operator.itemgetter(1)) # Sort the distances of animes
    neighbors = []
    for i in range(K):
        neighbors.append(distances[i][0])
    return neighbors

# def get_nearest_neighbors_by_rating(anime_id: int, K: int):
#     distances = []
#     anime_dictionary = anime_formatter()
    
#     for anime in anime_dictionary:
#         dist = get_distance(genre_list, anime[1]) 
#         distances.append((anime[0], dist))

#     distances.sort(key=operator.itemgetter(1)) # Sort the distances of animes
#     neighbors = []
#     for i in range(K):
#         neighbors.append(distances[i][0])
#     return neighbors