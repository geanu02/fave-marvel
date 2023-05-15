from flask import render_template, jsonify
from app import marvel_obj
from . import bp

@bp.route('/')
def home():
    return render_template(
        'index.jinja',
        title="Welcome to FaveMarvel",
    )
