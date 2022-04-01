import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root@localhost:3306/Recommender')
query = engine.execute('SELECT * FROM anime')

rows = query.fetchall()
anime = pd.DataFrame(rows)
print(anime)