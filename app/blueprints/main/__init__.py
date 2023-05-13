from flask import Blueprint
from config import Config
import hashlib
import requests
import datetime

from pprint import pprint as pp

bp = Blueprint('main', __name__)

timestamp = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S')
pub_key = Config.API_PUB_KEY
priv_key = Config.API_PRIV_KEY


def hash_params():
    """ Marvel API requires server side API calls to include
    md5 hash of timestamp + public key + private key """

    hash_md5 = hashlib.md5()
    hash_md5.update(f'{timestamp}{priv_key}{pub_key}'.encode('utf-8'))
    hashed_params = hash_md5.hexdigest()

    return hashed_params

params = {'ts': timestamp, 'apikey': pub_key, 'hash': hash_params()};
res = requests.get('https://gateway.marvel.com:443/v1/public/characters',
                   params=params)

results = res.json()
pp(results)

from app.blueprints.main import routes