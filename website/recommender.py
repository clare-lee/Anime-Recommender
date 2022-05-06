import json
import pandas as pd
import operator
from scipy import spatial
from .models import Anime

def anime_formatter():
    animelist = Anime.query.all()
    anime_dictionary = []

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
        dist = get_distance(genre_list, anime_dictionary[anime][1]) 
        distances.append((anime, dist))

    distances.sort(key=operator.itemgetter(1)) # Sort the distances of animes
    neighbors = []
    for i in range(K):
        neighbors.append(distances[i][0])
    return neighbors