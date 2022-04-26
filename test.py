import pandas as pd
from sqlalchemy import create_engine

# engine = create_engine('mysql+pymysql://root@localhost:3306/Recommender')
# query = engine.execute('SELECT * FROM anime')

# rows = query.fetchall()
# anime = pd.DataFrame(rows)

import numpy as np



df = pd.read_csv('anime.csv')


anime_genres = ['Action',
                'Adventure',
                'Cars',
                'Comedy',
                'Dementia',
                'Demons',
                'Drama',
                'Ecchi',
                'Fantasy',
                'Game',
                'Harem',
                'Hentai',
                'Historical',
                'Horror',
                'Josei',
                'Kids',
                'Magic',
                'Martial Arts',
                'Mecha',
                'Military',
                'Music',
                'Mystery',
                'Parody',
                'Police',
                'Psychological',
                'Romance',
                'Samurai',
                'School',
                'Sci-Fi',
                'Seinen',
                'Shoujo',
                'Shoujo Ai',
                'Shounen',
                'Shounen Ai',
                'Slice of Life',
                'Space',
                'Sports',
                'Super Power',
                'Supernatural',
                'Thriller',
                'Vampire',
                'Yaoi',
                'Yuri']
user_list = ['Adventure','Cars']

genre_list = pd.DataFrame(columns=['anime_id','Action',
                'Adventure',
                'Cars',
                'Comedy',
                'Dementia',
                'Demons',
                'Drama',
                'Ecchi',
                'Fantasy',
                'Game',
                'Harem',
                'Hentai',
                'Historical',
                'Horror',
                'Josei',
                'Kids',
                'Magic',
                'Martial Arts',
                'Mecha',
                'Military',
                'Music',
                'Mystery',
                'Parody',
                'Police',
                'Psychological',
                'Romance',
                'Samurai',
                'School',
                'Sci-Fi',
                'Seinen',
                'Shoujo',
                'Shoujo Ai',
                'Shounen',
                'Shounen Ai',
                'Slice of Life',
                'Space',
                'Sports',
                'Super Power',
                'Supernatural',
                'Thriller',
                'Vampire',
                'Yaoi',
                'Yuri'])

for x in df[['anime_id','genre']].iterrows():
    try:
        #print(x[1]['anime_id'])
        picked_genres = np.zeros(43).astype(int).tolist()
        for i in range(len(anime_genres)):
            if anime_genres[i] in x[1]['genre']:
                picked_genres[i] = 1
        
        #print(x[1]['anime_id'],picked_genres)
        picked_genres.insert(0,x[1]['anime_id'])
        genre_list.loc[genre_list.shape[0]]=picked_genres
    except TypeError:
        pass

print(genre_list)
genre_list.to_csv('genre.csv')