from app import app, login_manager, db, bcrypt
from .models import *
from .forms import *
from flask import request, redirect, render_template, flash
from flask_login import login_user, logout_user, current_user, login_required
import datetime
import logging


@app.route("/", methods=["GET", "POST"])
def scheduler():
    events = Event.query.order_by(Event._id).all()
    return render_template('scheduler.html', events=events, current_user=current_user)


# Login #
@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = CreateUserForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(email=email, username=username, password=bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect("/")
    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash('До новых встреч!')
    return redirect("/")


# Events
@app.route('/add', methods=["GET", "POST"])
def add_event():
    form = EventForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            subject = request.form.get('subject')
            description = request.form.get('description')
            date_start = request.form.get('date_start')
            date_end = request.form.get('date_end')
            event = Event(
                subject=subject,
                description=description,
                date_start=date_start,
                date_end=date_end,
                author=current_user.get_id())
            db.session.add(event)
            db.session.commit()
            return redirect("/")
    return render_template("add_event.html", form=form, date_start=datetime.datetime.now())


@app.route('/edit/<int:_id>', methods=["GET", "POST"])
def edit_event(_id):
    event = Event.query.filter(Event._id == int(_id)).first()
    form = EventForm(obj=event)
    if request.method == 'POST':
        if form.validate_on_submit():
            subject = request.form.get('subject')
            description = request.form.get('description')
            date_start = request.form.get('date_start')
            date_end = request.form.get('date_end')
            event.subject = subject
            event.description = description
            event.date_start = date_start
            event.date_end = date_end
            event.author = current_user.get_id()
            db.session.commit()
        return redirect("/")
    return render_template("add_event.html", form=form, date_start=datetime.datetime.now())


@app.route('/delete/<int:_id>', methods=["GET", "POST"])
def del_event(_id):
    if request.method == 'POST':
        event = Event.query.filter(Event._id == int(_id)).first()
        db.session.delete(event)
        db.session.commit()
    return redirect("/")
