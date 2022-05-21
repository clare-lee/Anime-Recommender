import json
import pandas as pd
import operator
import numpy as np
from scipy import spatial
from .models import Anime, User, Rating
from sqlalchemy.sql import func
from . import db


def anime_formatter():
    rating_df = pd.read_sql("SELECT * FROM rating", db.engine)
    ratings = rating_df.groupby('anime_id').agg({'rating': [np.size, np.mean]})
    rating_set = pd.DataFrame(ratings['rating']['size'])
    rating_set_norm = rating_set.apply(lambda x: (x-np.min(x) / (np.max(x) - np.min(x))))

    # combine values
    animelist = Anime.query.all()
    anime_dictionary = {}
    for anime in animelist:
        anime_dictionary[anime.anime_id]=[anime.name, [int(i) for i in anime.binary_genres.split(
            ",")], rating_set_norm.loc[anime.anime_id].get('size'), ratings.loc[anime.anime_id].get('mean')]


    return anime_dictionary

def get_distance(genre_1, genre_2):
    genre_similarity=spatial.distance.cosine(genre_1, genre_2)
    return genre_similarity

def get_distance_w_popularity(anime_1, anime_2):
    genre_similarity=spatial.distance.cosine(anime_1[1], anime_2[1])
    popularity_distance=abs(anime_1[2]-anime_2[2])
    return genre_similarity + popularity_distance

def get_nearest_neighbors(genre_list: list, K: int):
    distances=[]
    anime_dictionary=anime_formatter()

    for anime in anime_dictionary.values():
        dist=get_distance([0, genre_list, 1], anime)
        distances.append((anime[0], dist))

    distances.sort(key=operator.itemgetter(1))  # Sort the distances of animes
    neighbors=[]
    for i in range(K):
        neighbors.append(distances[i][0])
    return neighbors

# creates the recommendation based off users ratings from ideal genres list
def get_nearest_w_user(user_id: int, K: int):
    ratings = Rating.query.filter_by(user_id = user_id).all()
    genres_list = list(np.zeros(43))
    for rating in ratings:
        genres = [int(i) for i in rating.anime.binary_genres.split(",")]
        for i in range(43):
            genres_list[i] += genres[i] * rating.rating
    for i in range(43):
        genres_list[i] /= len(ratings)*10
        if genres_list[i] > 0.2 :
            genres_list[i] = 1
        else:
            genres_list[i] = 0
    return get_nearest_neighbors(genre_list, K)
