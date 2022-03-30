from flask import Blueprint, render_template
from .models import Anime
from flask_login import login_required, current_user
views = Blueprint('views', __name__)


@views.route('/')
def home():     # this function will run whenever we go to route
    return render_template("home.html")
    
@views.route('/anime')
def anime_view():
    print(Anime.__table__)
    animelist = Anime.query.all()
    return render_template("anime.html", animelist = animelist)

@views.route('/recommendation')
def anime_view():
    print(Anime.__table__)
    recommendation = Anime.query.all()
    return render_template("recommendation.html", recommendation = recommendation)