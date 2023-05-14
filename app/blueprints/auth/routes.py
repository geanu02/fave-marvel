from flask import render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

from . import bp
from app.forms import SignUpForm, SigninForm


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SignUpForm()
    if form.validate_on_submit():
        input_email = form.email.data
        input_username = form.username.data
        email_check = User.query.filter_by(email=input_email).first()
        username_check = User.query.filter_by(username=input_username).first()
        if not email_check and not username_check:
            u = User(
                email=input_email,
                username=input_username,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )
            u.password = u.hash_password(form.password.data)
            u.add_token()
            u.commit()
            flash(f"{input_username} successfully registered!", "success")
            user_login = User.query.filter_by(username=form.username.data).first()
            flash(f"Welcome to Marvel Favorites, {user_login.first_name}!", "success")
            login_user(user_login)
            return redirect(url_for("marvel.search_marvel"))
        elif email_check and not username_check:
            flash(f"{input_email} already registered. Try again.", "warning")
        elif not email_check and username_check:
            flash(f"{input_username} already registered. Try again.", "warning")
        else:
            flash("Something went wrong. Try again.", "warning")
    return render_template(
        'signup.jinja',
        title="Register",
        form=form
    )


@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        check_pass = user.check_password(form.password.data)
        if user and check_pass:
            flash(f"Welcome back, {user.first_name}! You are signed in!", "success")
            login_user(user)
            return redirect(url_for("marvel.search_marvel"))
        if not user and check_pass:
            flash(
                f"{form.username.data} not registered.", "warning")
        else:
            flash("Password incorrect.", "warning")
    return render_template(
        'signin.jinja',
        title="Signin",
        form=form
    )


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))