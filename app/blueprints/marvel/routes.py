from flask import render_template, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required
from app import db, marvel_obj
from . import bp

from app.models import User, FaveMarvel, Marvel
from app.forms import SearchForm, MarvelForm


@bp.route('/marvel', methods=["GET", "POST"])
def search_marvel():
    form = SearchForm()
    if form.validate_on_submit():
        input_name = form.marvel_char.data
        results = marvel_obj.characters.all(nameStartsWith=input_name)[
            'data']['results']
        if results:
            return render_template(
                'marvel.jinja',
                title="Marvel Characters",
                form=form,
                chars=results
            )
    return render_template(
        'marvel.jinja',
        title="Marvel Characters",
        form=form
    )


@bp.route('/add/<marvel_id>', methods=["GET", "POST"])
@login_required
def add_marvel(marvel_id):
    m_in_db = Marvel.query.filter_by(marvel_id=marvel_id).first()
    user = User.query.filter_by(username=current_user.username).first()
    if marvel_id in [mar.marvel_id for mar in user.fave_marvel]:
        nick = filter(lambda x: x.marvel_id == marvel_id, user.fave_marvel)
        flash(
            f"{nick.nickname.title()} is already in your favorites. Try another one?", "success")
        return redirect(url_for("marvel.search_marvel"))
    if m_in_db:
        results = m_in_db
    else:
        dta = marvel_obj.characters.get(marvel_id)['data']['results'][0]
        name = dta['name'].title()
        desc = dta['description']
        img = '.'.join([dta['thumbnail']['path'],
                       dta['thumbnail']['extension']])
        comic = dta['comics']['available']
        m_new = Marvel(marvel_id=marvel_id, m_name=name)
        m_new.m_desc = desc if desc else "No description available."
        m_new.m_img = img
        m_new.m_comics = comic
        m_new.commit()
        flash(f"{name} is added to the Marvel database!", "success")
        results = m_new
    form = MarvelForm()
    if form.validate_on_submit():
        nickname = form.nickname.data if form.nickname.data else results.m_name
        superpower = form.superpower.data if form.superpower.data else "No Superpower"
        fm = FaveMarvel(
            m_name=results.m_name,
            nickname=nickname,
            superpower=superpower,
            marvel_id=marvel_id,
            user_id=user.user_id
        )
        fm.commit()
        flash(f"{nickname} is added to your favorites!", "success")
    return render_template(
        'add_marvel.jinja',
        title=f"{user.first_name}'s Favorite Marvel Characters",
        user=user,
        form=form,
        results=results
    )


@bp.route('/<username>', methods=["GET", "POST"])
@login_required
def user_page(username):
    user = User.query.filter_by(username=username).first()
    if FaveMarvel.query.filter_by(user_id=current_user.user_id).first():
        fave_marvel = db.session.query(FaveMarvel, Marvel).join(Marvel).filter(FaveMarvel.user_id == current_user.user_id).all()
        return render_template(
            'user_page.jinja',
            title="Favorite Marvel Characters",
            fave_marvel=fave_marvel,
            user=user
        )
    return render_template(
        'user_page.jinja',
        title="Favorite Marvel Characters",
        user=user
    )
