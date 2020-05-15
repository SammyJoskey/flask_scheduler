  
from datetime import datetime
import functools
from flask import jsonify, render_template, request, redirect, flash, url_for, session

from app import app, db, login_manager, bcrypt
from .models import Event, User
from .forms import EventForm, LoginForm


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                session["email"] = form.email.data
                return redirect("/")
    return render_template("login.html", form=form)


@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        user = User(email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        return redirect("/")
    return render_template("create.html", form=form)



@app.route('/')
@app.route('/schedule', methods=["GET", "POST"])
@login_required
def schedule():
    events = db.session.query(Event).order_by(Event.start.desc()).all()
    return render_template('schedule.html', events=events)


@app.route('/event', methods=['POST', 'GET'])
@login_required
def event():
    event_form = EventForm()
    if request.method == 'POST':
        if event_form.validate_on_submit():
            author = session['email']
            start = request.form.get('start')
            start_format = datetime.strptime(start, '%Y-%m-%d %H:%M')
            end = request.form.get('end')
            end_format = datetime.strptime(end, '%Y-%m-%d %H:%M')
            subject = request.form.get('subject')
            description = request.form.get('description')
            event = Event(
                author=author, 
                start=start_format, 
                end=end_format, 
                subject=subject, 
                description=description)
            db.session.add(event)
            db.session.commit()
            return redirect('/')
        error = "Form was not validated"
        return render_template('error.html',form=event_form, error = error)        
    return render_template('add_event.html', form=event_form)

@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def event_update(event_id):
    event = db.session.query(Event).filter(Event._id==int(event_id)).first()
    event_form = EventForm(obj=event)
    if request.method == 'POST':
        if event and event_form.validate(): 
                author = request.form.get('author')
                if author != session['email']:
                    error = "Forbidden event to edit"
                    return render_template('error.html',form=event_form, error = error)
                start = request.form.get('start')
                start_format = datetime.strptime(start, '%Y-%m-%d %H:%M')
                end = request.form.get('end')
                end_format = datetime.strptime(end, '%Y-%m-%d %H:%M')
                subject = request.form.get('subject')
                description = request.form.get('description')
                event.author = author
                event.subject = subject
                event.description = description
                event.start = start_format
                event.end = end_format
                db.session.commit()
                return redirect('/')
        error = "Form was not validated"
        return render_template('error.html',form=event_form, error = error)        
    return render_template('edit_event.html', form=event_form)