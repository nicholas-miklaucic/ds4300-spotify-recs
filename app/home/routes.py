from flask import Blueprint, render_template, current_app
from app.db import get_db, get_feats, get_spotify
from app.home.spotify import playlist_data
import numpy as np
import json

home = Blueprint("home", __name__)


@home.route("/home")
@home.route("/", methods=["GET", "POST"])
def homepage():
    return render_template("home.html", title="Home")


@home.route("/playlist/<playlist_id>")
def recs(playlist_id):
    f = open('songs.json')
    songs = json.load(f)

    song_urls = []
    for song in songs:
        curr = song["external_urls"]["spotify"]
        new_url = curr[0:25] + "embed/" + curr[25:]
        song_urls.append(new_url)

    print(songs)
    return render_template("results.html", data=song_urls, title="Results")
    '''
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
    '''
    return "hello"
