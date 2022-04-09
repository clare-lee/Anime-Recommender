import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root@localhost:3306/Recommender')
query = engine.execute('SELECT * FROM anime')

rows = query.fetchall()
anime = pd.DataFrame(rows)

anime_tv = anime.loc[anime['medium'] == 'TV']
anime_tv = anime_tv.sort_values(by='rating', ascending=False)
anime_tv.reset_index(drop=True, inplace=True)

print(anime_tv.head(10))