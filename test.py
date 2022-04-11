import pandas as pd
from sqlalchemy import create_engine

# engine = create_engine('mysql+pymysql://root@localhost:3306/Recommender')
# query = engine.execute('SELECT * FROM anime')

# rows = query.fetchall()
# anime = pd.DataFrame(rows)

import numpy as np

picked_genres = np.zeros(43)

anime_genres = ['Action',
 'Adventure',
 'Comedy',
 'Drama',
 'Sci-Fi',
 'Space',
 'Mystery',
 'Magic',
 'Police',
 'Supernatural',
 'Fantasy',
 'Shounen',
 'Sports',
 'Josei',
 'Romance',
 'Slice of Life',
 'Cars',
 'Seinen',
 'Horror',
 'Psychological',
 'Thriller',
 'Martial Arts',
 'Super Power',
 'School',
 'Ecchi',
 'Vampire',
 'Historical',
 'Military',
 'Dementia',
 'Mecha',
 'Demons',
 'Samurai',
 'Game',
 'Shoujo',
 'Harem',
 'Music',
 'Shoujo Ai',
 'Shounen Ai',
 'Kids',
 'Hentai',
 'Parody',
 'Yuri',
 'Yaoi']

user_list = ['Hentai', 'Yaoi']

print(len(anime_genres))
for g in user_list:
    for i in range(len(anime_genres)):
        if g == anime_genres[i]:
            picked_genres[i] = 1
            
print(picked_genres)