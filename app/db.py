#!/usr/bin/env python3

import pymongo
import numpy as np
from tqdm import tqdm
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


from flask import current_app, g, Flask
from flask.cli import with_appcontext


app = Flask(__name__)


def get_db():
    if "db" not in g:
        client = pymongo.MongoClient(current_app.config["MONGODB_URL"])
        g.db = (client, client["Cluster0"]["spotifySongs"])

    return g.db


def get_spotify():
    if "sp" not in g:
        CLIENT_ID = current_app.config["SPOTIFY_CLIENT_ID"]
        CLIENT_SECRET = current_app.config["SPOTIFY_CLIENT_SECRET"]

        g.sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=CLIENT_ID, client_secret=CLIENT_SECRET
            )
        )
    return g.sp


def get_feats(mu, sd):
    if "feats" not in g:
        (_client, songs) = get_db()

        all_feats = []
        all_ids = []

        query = {}
        for feat_name, m, s in zip(
            current_app.config["FEAT_NAMES"], mu.flatten(), sd.flatten()
        ):
            query[feat_name] = {"$gt": m - 1 * s, "$lt": m + 1 * s}

        print(query)

        with tqdm(songs.find(query), total=songs.estimated_document_count(),) as docs:
            for doc in docs:
                all_feats.append(
                    np.array(
                        [
                            doc[feat_name]
                            for feat_name in current_app.config["FEAT_NAMES"]
                        ]
                    )
                )
                all_ids.append(doc["id"])

        g.feats = (np.array(all_feats), np.array(all_ids))

    return g.feats


def close_db(e=None):
    db, _songs = g.pop("db", None)

    if db is not None:
        db.close()


def init_app(app: Flask):
    app.before_first_request(get_feats)
    app.teardown_appcontext(close_db)
