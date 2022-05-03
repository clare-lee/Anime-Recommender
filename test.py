import pandas as pd
from sqlalchemy import create_engine

# engine = create_engine('mysql+pymysql://root@localhost:3306/Recommender')
# query = engine.execute('SELECT * FROM anime')

# rows = query.fetchall()
# anime = pd.DataFrame(rows)

import numpy as np



df = pd.read_csv('anime.csv')
df2 = pd.read_csv('anime_original.csv').set_index("anime_id")

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

df['binary_genres'] = "sas"
df['popularity'] = 0
df = df.set_index("anime_id")
for x in df[['anime_id','genre']].iterrows():
    try:
        #print(x[1]['anime_id'])
        picked_genres = np.zeros(43).astype(int).tolist()
        for i in range(len(anime_genres)):
            if anime_genres[i] in x[1]['genre']:
                picked_genres[i] = 1
       
        df.at[x[0], 'binary_genres'] = ", ".join([str(i) for i in picked_genres])
        
    except TypeError:
        print("type error")


df['popularity'] = df2['members'] 
df.to_csv('anime2.csv')/Users/chick/Recommender-System/anime.csv