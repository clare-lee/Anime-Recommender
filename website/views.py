from flask import Blueprint, render_template, request
from .models import Anime
from flask_login import login_required, current_user
import pandas as pd
from sqlalchemy import create_engine
from recommender import get_nearest_neighbors


views = Blueprint('views', __name__)

genre_list = {
    'genre1':'Action',
    'genre2':'Adventure',
    'genre3':'Cars',
    'genre4':'Comedy',
    'genre5':'Dementia',
    'genre6':'Demons',
    'genre7':'Drama',
    'genre8':'Ecchi',
    'genre9':'Fantasy',
    'genre10':'Game',
    'genre11':'Harem',
    'genre12':'Hentai',
    'genre13':'Historical',
    'genre14':'Horror',
    'genre15':'Josei',
    'genre16':'Kids',
    'genre17':'Magic',
    'genre18':'Martial Arts',
    'genre19':'Mecha',
    'genre20':'Military',
    'genre21':'Music',
    'genre22':'Mystery',
    'genre23':'Parody',
    'genre24':'Police',
    'genre25':'Psychological',
    'genre26':'Romance',
    'genre27':'Samurai',
    'genre28':'School',
    'genre29':'Sci-Fi',
    'genre30':'Seinen',
    'genre31':'Shoujo',
    'genre32':'Shoujo Ai',
    'genre33':'Shounen',
    'genre34':'Shounen Ai',
    'genre35':'Slice of Life',
    'genre36':'Space',
    'genre37':'Sports',
    'genre38':'Super Power',
    'genre39':'Supernatural',
    'genre40':'Thriller',
    'genre41':'Vampire',
    'genre42':'Yaoi',
    'genre43':'Yuri'
}

@views.route('/')
def home():     # this function will run whenever we go to route
    engine = create_engine('mysql+pymysql://root@localhost:3306/Recommender')
    query = engine.execute('SELECT * FROM anime')

    rows = query.fetchall()
    anime = pd.DataFrame(rows)

    # The highest rated TV-series
    anime_tv = anime.loc[anime['medium'] == 'TV']
    anime_tv = anime_tv.sort_values(by='rating', ascending=False)
    anime_tv.reset_index(drop=True, inplace=True)
    tvs = anime_tv.head(10)
    tvs = tvs['name']

    # The highest rated Movies
    anime_movie = anime.loc[anime['medium'] == 'Movie']
    anime_movie = anime_movie.sort_values(by='rating', ascending=False)
    anime_movie.reset_index(drop=True, inplace=True)
    mvs = anime_movie.head(10)
    mvs = mvs['name']

    # The highest rated OVA
    anime_ova = anime.loc[anime['medium'] == 'OVA']
    anime_ova = anime_ova.sort_values(by='rating', ascending=False)
    anime_ova.reset_index(drop=True, inplace=True)
    ovs = anime_ova.head(10)
    ovs = ovs['name']

    return render_template("home.html", best_list=zip(tvs,mvs,ovs))

@views.route('/anime')
def anime_view():
    print(Anime.__table__)
    animelist = Anime.query.all()
    return render_template("anime.html", animelist = animelist)

@views.route('/recommendation')
def recommendation():

    return render_template("recommendation.html")

# recommendation
@views.route('/title_search', methods=['POST'])
def search():
    engine = create_engine('mysql+pymysql://root@localhost:3306/Recommender')
    query = engine.execute('SELECT * FROM anime')

    rows = query.fetchall()
    anime = pd.DataFrame(rows)

    return request.form['anime_title']
    
# recommendation
@views.route('/genre_search', methods=['POST'])
def genre_search():
    genres = []

    for i in range(1,44):
        if request.form.get(f'genre{i}') is not None:
            genres.append(1)
        else:
            genres.append(0)

    neighbors = get_nearest_neighbors(genre,10)

    #create log here 
    
    return str(neighbors)