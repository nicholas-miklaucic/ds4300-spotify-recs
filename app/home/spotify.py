#!/usr/bin/env python3

from flask import current_app
from app.db import get_spotify
import numpy as np
import pandas as pd

FEAT_NAMES = [
    "danceability",
    "energy",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "valence",
    "tempo",
]

WEIGHTS = np.ones_like(FEAT_NAMES, dtype=np.float32)


def playlist_data(playlist_id):
    sp = get_spotify()
    feats_df = []

    pl = sp.playlist(playlist_id)
    for x in pl["tracks"]["items"]:
        feats = sp.audio_features(x["track"]["id"])[0]
        feats_df.append(feats)

    feats_df = pd.DataFrame(feats_df)

    vals = feats_df[current_app.config["FEAT_NAMES"]]
    mu = vals.mean(axis=0).values.reshape(1, -1)
    sd = vals.std(axis=0).values.reshape(1, -1)
    return (mu, sd)
