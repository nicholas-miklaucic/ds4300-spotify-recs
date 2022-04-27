from flask import Blueprint, render_template, current_app
from app.db import get_db, get_feats, get_spotify
from app.home.spotify import playlist_data
import numpy as np

home = Blueprint("home", __name__)


@home.route("/home")
@home.route("/", methods=["GET", "POST"])
def homepage():
    return render_template("home.html", title="Home")


@home.route("/playlist/<playlist_id>")
def recs(playlist_id):
    mu, sd = playlist_data(playlist_id)
    w = current_app.config["WEIGHTS"]
    feats, ids = get_feats()
    dists = np.sum(w * np.square((feats - mu) / sd), axis=1)

    top_n = 50

    ranks = np.argsort(dists)[:top_n]
    sp = get_spotify()
    names = []
    for song_id in ids[ranks]:
        song = sp.track(song_id)
        names.append(song["name"] + " " + song["artists"][0]["name"])

    return "\n".join(names)
