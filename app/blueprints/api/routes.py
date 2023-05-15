from flask import jsonify, make_response
import json
from . import bp
from app import db
from app.models import User, FaveMarvel, Marvel, MarvelSchema
from app.blueprints.api.helpers import token_required

# Initialize Schemas
marvel_schema = MarvelSchema()
marvels_schema = MarvelSchema(many=True)

# Receive All Marvel Characters
@bp.get('/marvel')
@token_required
def marvel_all(user):
    marvel = Marvel.query.all()
    if marvel:
        result = marvels_schema.dump(marvel)
        return jsonify(result)
    # if marvel:
    #     result = []
    #     for m in marvel:
    #         result.append({
    #             'id': m.id,
    #             'marvel_id': m.marvel_id,
    #             'marvel_name': m.m_name,
    #             'marvel_desc': m.m_desc,
    #             'marvel_img': m.m_img,
    #             'marvel_comics': m.m_comics
    #         })
    #     return make_response(jsonify(result), 200)
    # else:
    #     return jsonify([{'message':'No characters available to view.'}]), 404

# Receive Marvel Character by marvel_id
@bp.get('/marvel/<marvel_id>')
@token_required
def marvel_single_id(user, marvel_id):
    m = Marvel.query.filter_by(marvel_id=marvel_id).first()
    if m:
        return jsonify([{
            'id': m.id,
            'marvel_id': m.marvel_id,
            'marvel_name': m.m_name,
            'marvel_desc': m.m_desc,
            'marvel_img': m.m_img,
            'marvel_comics': m.m_comics
        }]), 200
    return jsonify([{'message':'No characters available to view.'}]), 404

# Receive All Favorite Marvel Characters from User by username
@bp.get('/marvel/<username>/')
@token_required
def marvel_all_by_user(user, username):
    if user.username == username:
        join_fave_marvel = db.session.query(FaveMarvel, Marvel).join(Marvel).filter(FaveMarvel.user_id == user.user_id).all()
        if join_fave_marvel:
            return jsonify([{
                'user_id': user.user_id,
                'username': user.username,
                'fave_id': f.fave_id,
                'fave_added': f.date_added,
                'fave_nickname': f.nickname,
                'fave_superpower': f.superpower,
                'marvel_id': m.marvel_id,
                'marvel_name': m.m_name,
                'marvel_desc': m.m_desc,
                'marvel_img': m.m_img,
                'marvel_comics': m.m_comics
            } for f, m in join_fave_marvel]), 200
        return jsonify([{'message' : '{username} does not have favorites.'}]), 404
    return jsonify([{'message' : 'Invalid username.'}]), 404

# Receive Favorite Marvel Character by marvel_id from User by username
@bp.get('/marvel/<username>/<marvel_id>')
@token_required
def marvel_single_id_by_user(user, username, marvel_id):
    if user.username == username:
        if Marvel.query.filter_by(marvel_id=marvel_id).first():
            join_fave_marvel = db.session.query(FaveMarvel, Marvel).join(Marvel).filter(FaveMarvel.user_id == user.user_id, FaveMarvel.marvel_id == marvel_id).all()
            if join_fave_marvel:
                return jsonify([{
                    'user_id': user.user_id,
                    'username': user.username,
                    'fave_id': f.fave_id,
                    'fave_added': f.date_added,
                    'fave_nickname': f.nickname,
                    'fave_superpower': f.superpower,
                    'marvel_id': m.marvel_id,
                    'marvel_name': m.m_name,
                    'marvel_desc': m.m_desc,
                    'marvel_img': m.m_img,
                    'marvel_comics': m.m_comics
                } for f, m in join_fave_marvel]), 200
            return jsonify([{'message' : '{username} does not have favorites.'}]), 404
        return jsonify([{'message' : '{marvel_id} not registered.'}]), 404
    return jsonify([{'message' : 'Invalid username.'}]), 404
