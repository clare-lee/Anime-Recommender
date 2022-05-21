from flask import Blueprint, render_template, request, flash, redirect
from .models import Anime, Log, Favs, Rating
from flask_login import login_required, current_user
import pandas as pd
from .recommender import get_nearest_neighbors, get_nearest_w_user
from . import db

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

# general recommendation @home
@views.route('/')
def home():    
    
    rows = Anime.query.all()

    anime = pd.DataFrame([vars(r) for r in rows])

    # The highest rated and most popular TV-series
    anime_tv = anime.loc[anime['medium'] == 'TV']
    # Selects most popular 
    anime_tv = anime_tv.nlargest(30,'members')
    # Sorts highest rated
    anime_tv = anime_tv.sort_values(by='rating', ascending=False)
    anime_tv.reset_index(drop=True, inplace=True)
    tvs = anime_tv.head(10)
    tvs = tvs['name']

    # The highest rated Movies
    anime_movie = anime.loc[anime['medium'] == 'Movie']
    # Selects most popular 
    anime_movie = anime_movie.nlargest(30,'members')
    # Sorts highest rated
    anime_movie = anime_movie.sort_values(by='rating', ascending=False)
    anime_movie.reset_index(drop=True, inplace=True)
    mvs = anime_movie.head(10)
    mvs = mvs['name']

    # The highest rated OVA
    anime_ova = anime.loc[anime['medium'] == 'OVA']
    # Selects most popular 
    anime_ova = anime_ova.nlargest(30,'members')
    # Sorts highest rated
    anime_ova = anime_ova.sort_values(by='rating', ascending=False)
    anime_ova.reset_index(drop=True, inplace=True)
    ovs = anime_ova.head(10)
    ovs = ovs['name']

    return render_template("home.html", best_list=zip(tvs,mvs,ovs), user=current_user)

@views.route('/anime')
def anime_view():
    animelist = Anime.query.all()
    return render_template("anime.html", animelist = animelist, user=current_user)

@views.route('/recommendation', methods=['GET'])
@login_required 
def recommendation():
    anime = Anime.query.all()
    return render_template("recommendation.html", user=current_user, anime = [i.name for i in anime])

# recommendation by anime title
@views.route('/title_search', methods=['POST'])
@login_required 
def search():
    
    anime = Anime.query.filter_by(name = request.form.get("anime_title")).first()

    if anime is None:
        return render_template('/recommendation.html', animelist=[], user=current_user, error = "Anime name not found")

    binary_genres = [int(i) for i in anime.binary_genres.split(",")]
    # using recommender.py
    #neighbors = get_nearest_neighbors(binary_genres,11)
    neighbors = find_neighbors(anime,11)
    del neighbors[0]    # remove searched title from recommendations
    
    # create log 
    log = Log(
        data = str(neighbors),
        user_id = current_user.get_id()
    )

    # post to db
    db.session.add(log)
    db.session.commit()

    return render_template('/viewSearch.html', animelist=neighbors, user=current_user)
    
# recommendation by genre selection
@views.route('/genre_search', methods=['POST'])
@login_required
def genre_search():

    # convert user's genre selection into list of binary_genres
    genres = []
    for i in range(1,44):
        if request.form.get(f'genre{i}') is not None:
            genres.append(1)
        else:
            genres.append(0)

    neighbors = get_nearest_neighbors(genres,10)

    #create log 
    log = Log(
        data = str(neighbors),
        user_id = current_user.get_id()
    )

    # post to db
    db.session.add(log)
    db.session.commit()

    return render_template('/viewSearch.html', animelist=neighbors, user=current_user)

# view log of all user's recommendations
@views.route('/view', methods=['GET'])
@login_required
def view_log():
    # view logs sorted by recent
    logs = Log.query.filter_by(user_id = current_user.get_id()).order_by(Log.date.desc()).all()
    favs = Favs.query.filter_by(user_id = current_user.get_id()).all()
    anime = Anime.query.all()
    ratings = Rating.query.filter_by(user_id = current_user.get_id()).all()
    ratings.sort(key=lambda x: x.anime.name)
    return render_template('/view.html', logs = logs, user = current_user, favs = favs, anime = [i.name for i in anime], ratings = ratings)

# user adds favorite anime
@views.route('/view', methods=['POST'])
@login_required
def save_favs():
    if request.method == 'POST':
        favs = request.form.get('fav')

        if len(favs) < 1:
            flash('Invalid Entry', category='error')
        else:
            new_fav = Favs(data=favs, user_id=current_user.id)
            db.session.add(new_fav)
            db.session.commit()
            flash('Favorite Added', category='success')

    return redirect('/view')

# user deletes favorite anime    
@views.route('/view', methods=['DELETE'])
@login_required
def delete_fav(): 
    if request.method == 'DELETE':
        favid = request.json['favid']
        fav = Favs.query.filter_by(id = favid).first()
        print(fav)
        if fav is not None:
            db.session.delete(fav)
            db.session.commit()
            flash("Favorite Removed", category='success')

    return view_log()

# user adds rating
@views.route('/rate', methods=['POST'])
@login_required
def add_rating():
    if request.method == 'POST':
        rating = request.form.get('rating')
        anime = request.form.get('anime')

        if len(anime) < 1:
            flash('Invalid Entry', category='error')
        else:
            Animeobj = Anime.query.filter_by(name = anime).first()
            new_rating = Rating(rating=rating, anime_id=Animeobj.anime_id, user_id=current_user.id)
            db.session.add(new_rating)
            db.session.commit()
            flash('Anime rated!', category='success')

    return redirect('/view')
