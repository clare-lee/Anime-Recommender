from flask import Blueprint, render_template
from .models import Anime
from flask_login import login_required, current_user
import pandas as pd
from sqlalchemy import create_engine
views = Blueprint('views', __name__)


@views.route('/')
def home():     # this function will run whenever we go to route
    engine = create_engine('mysql+pymysql://root@localhost:3306/Recommender')
    query = engine.execute('SELECT * FROM anime')

    rows = query.fetchall()
    anime = pd.DataFrame(rows)

    # The highiest rated TV-series
    anime_tv = anime.loc[anime['medium'] == 'TV']
    anime_tv = anime_tv.sort_values(by='rating', ascending=False)
    anime_tv.reset_index(drop=True, inplace=True)
    tvs = anime_tv.head(10)
    print(tvs)
    return render_template("home.html", tvs = tvs)
    
@views.route('/anime')
def anime_view():
    print(Anime.__table__)
    animelist = Anime.query.all()
    return render_template("anime.html", animelist = animelist)


# @views.route('/recommendation')
# def anime_view():
#     print(Anime.__table__)
#     recommendation = Anime.query.all()
#     return render_template("recommendation.html", recommendation = recommendation)