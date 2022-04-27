import os
import string
import random
import numpy as np


import pandas as pd


letters = string.ascii_letters


class BaseConfig(object):
    """base config"""

    SECRET_KEY = os.environ.get(
        "secret_key",
        "".join(
            [random.choice(string.ascii_letters + string.digits) for n in range(16)]
        ),
    )
    MONGODB_URL = os.environ.get("MONGODB_URL")
    SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

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


class TestingConfig(BaseConfig):
    """testing config"""

    TESTING = True
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    """dev config"""

    DEBUG = True


class ProductionConfig(BaseConfig):
    """production config"""
