import json
import pandas as pd
import operator
import numpy as np
from scipy import spatial
from sklearn import preprocessing
from .models import Anime, User, Rating, Log
from flask_login import current_user
from sqlalchemy.sql import func
from . import db


def get_distance(genre_1, genre_2):
    # fix issue of all 0 genres binary from having 0 distance
    if sum(genre_1) == 0 or sum(genre_2) == 0:
        return 1
    genre_similarity = spatial.distance.cosine(genre_1, genre_2)
    return genre_similarity

def anime_formatter():
    # create a df containing averaged normalized anime ratings
    rating_df = pd.read_sql("SELECT * FROM rating", db.engine)
    ratings = rating_df.groupby('anime_id').agg({'rating': [np.size, np.mean]})
    rating_set = pd.DataFrame(ratings['rating']['size'])
    rating_set_norm = rating_set.apply(lambda x: (x-np.min(x) / (np.max(x) - np.min(x))))

    # combine values into a usable dictionary
    animelist = Anime.query.all()
    anime_dictionary = {}
    for anime in animelist:
        anime_dictionary[anime.anime_id]=[anime.name, [int(i) for i in anime.binary_genres.split(
            ",")], rating_set_norm.loc[anime.anime_id].get('size'), 
            ratings.loc[anime.anime_id].get('mean'), anime.members]
    return anime_dictionary

def get_distance_w_popularity(anime_1, anime_2):
    if sum(anime_1[1]) == 0 or sum(anime_2[1]) == 0:
        return 1
    # gets distance based on how genre similarity
    genre_similarity = spatial.distance.cosine(anime_1[1], anime_2[1])
    # gets how close animes are
    popularity_distance = abs(anime_1[2]-anime_2[2])
    return genre_similarity*2 + popularity_distance + anime_2[4]

# creates recommendation on similar genres
def get_nearest_neighbors(anime_, K: int):
    distances=[]

    logs = Log.query.filter_by(user_id=current_user.get_id()).all()

    anime_dictionary = anime_formatter()
    filtered = []

    for log in logs:
        filtered.extend(eval(log.data))

    filtered = set(filtered)

    filtered_dictionary = [i for i in anime_dictionary.values() if not i[0] in filtered]

    # to weigh anime member higher
    members_max = 0
    for anime in filtered_dictionary:
        if anime[4] > members_max:
            members_max = anime[4]

    for anime in filtered_dictionary:
        anime[4] = 1-(anime[4]/members_max)

    test = anime_
    if anime_[0] != 0:
        test = anime_dictionary[anime_[0]]
    # gets distances of all animes
    for anime in filtered_dictionary:  
        if test[0] == anime[0]:
            continue     
        dist = get_distance_w_popularity(test, anime)
        distances.append((anime[0], dist))

    # organizes animes by thoses with closest distance or most similar animes
    distances.sort(key=operator.itemgetter(1))  
    neighbors = []

    # gets K number of animes
    for i in range(K):
        neighbors.append(distances[i][0])

    return neighbors

# creates the recommendation based off users ratings from ideal genres list
def get_nearest_w_user(user_id: int, K: int):
    
    # gets all ratings by current user
    ratings = Rating.query.filter_by(user_id = user_id).all()
    genres_list = list(np.zeros(43))

    # generates a projected desired genre set based off user's ratings
    for rating in ratings:  # combine user's genre's search genres with ratings' genres
        genres = [int(i) for i in rating.anime.binary_genres.split(",")]
        for i in range(43):
            genres_list[i] += genres[i] * rating.rating
    for i in range(43):
        genres_list[i] /= len(ratings)*10
        if genres_list[i] > 0.2:
            genres_list[i] = 1
        else:
            genres_list[i] = 0
    return get_nearest_neighbors([0, genres_list, 1], K)
