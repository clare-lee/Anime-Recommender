import json
import pandas as pd
import operator
import numpy as np
from scipy import spatial
from sklearn import preprocessing
from .models import Anime, User, Rating
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
            ratings.loc[anime.anime_id].get('mean')]
    return anime_dictionary

def get_distance_w_popularity(anime_1, anime_2):
    if sum(anime_1[1]) == 0 or sum(anime_2[1]) == 0:
        return 1
    # gets distance based on how genre similarity
    genre_similarity = spatial.distance.cosine(anime_1[1], anime_2[1])
    # gets how close animes are
    popularity_distance = abs(anime_1[2]-anime_2[2])
    return genre_similarity*2 + popularity_distance

# creates recommendation on similar genres
def get_nearest_neighbors(anime_, K: int):
    distances=[]
    anime_dictionary = anime_formatter()
    test = anime_
    if anime_[0] != 0:
        test = anime_dictionary[anime_[0]]
    # gets distances of all animes
    for anime in anime_dictionary.values():  
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

def get_genre_distance(anime_one, anime_two):
    genre_similarity = 0
    isValid = 1
    same_type = 1
   
    genre_one = [int(i) for i in anime_one.binary_genres.split(',')]
    genre_two = [int(i) for i in anime_two.binary_genres.split(',')]


    genre_similarity = spatial.distance.cosine(genre_one, genre_two)
    return genre_similarity

# gets distance using anime rating
def get_rating_distance(anime_1, anime_2):
    rating_distance = 0.0
    if (([not s or s.isspace() for s in anime_1[5]]) and ([not sp or sp.isspace() for sp in anime_2[5]])):
        rating_distance += ((float(anime_1[5])/10) - (float(anime_2[5])/10))**2
    return rating_distance

# get distance using popularity
def get_members_distance(anime_1, anime_2):
    members_distance = 0.0

    members_array = np.array([[int(anime_1.members), int(anime_2.members)]])
    members_array = preprocessing.normalize(members_array)
    members_distance += (members_array[0][0] - members_array[0][1])**2
    return members_distance

# get's total distance 
def calc_euclidean_distance(anime_1, anime_2):
    genre_distance = get_genre_distance(anime_1, anime_2)
    members_distance = get_members_distance(anime_1, anime_2)
    rating_distance = get_rating_distance(anime_1, anime_2)
    total_distance = (genre_distance + rating_distance + members_distance)
    print("Total distance between \"",anime_1[1], "\" and \"", anime_2[1], "\": ", total_distance, '\n')
    return total_distance

# creates recommendation on rating, pop, genres
def find_neighbors(test_anime, k_neighbors):
    distances = list()
    animes = pd.read_sql("SELECT * FROM anime", db.engine)
    #animes = load_csv("anime.csv")
    for index, anime in animes.iterrows():
        calculated_distance = calc_euclidean_distance(test_anime, anime)
        distances.append((anime[1], calculated_distance))    
    distances.sort(key=lambda tup: tup[1])
    neighbors = list()
    for i in range(k_neighbors):
        neighbors.append(distances[i][0])
    return neighbors
