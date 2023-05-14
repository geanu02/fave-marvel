from flask import Blueprint

bp = Blueprint('marvel', __name__)

from app.blueprints.marvel import routes
