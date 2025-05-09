from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "diary.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    entries = db.relationship('Entry', backref='author', lazy=True)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    mood = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Forms
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    mood = SelectField('Mood', choices=[
        ('happy', 'Happy 😊'),
        ('sad', 'Sad 😢'),
        ('angry', 'Angry 😠'),
        ('excited', 'Excited 🤩'),
        ('neutral', 'Neutral 😐')
    ], validators=[DataRequired()])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
@login_required
def dashboard():
    entries = Entry.query.filter_by(user_id=current_user.id).order_by(Entry.date.desc()).all()
    return render_template('dashboard.html', entries=entries, form=EntryForm())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password', 'error')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'error')
            return render_template('register.html', form=form)
        
        user = User(
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/entry/new', methods=['POST'])
@login_required
def new_entry():
    form = EntryForm()
    if form.validate_on_submit():
        entry = Entry(
            title=form.title.data,
            content=form.content.data,
            mood=form.mood.data,
            user_id=current_user.id
        )
        db.session.add(entry)
        db.session.commit()
        flash('Entry saved successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/entry/<int:entry_id>')
@login_required
def view_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    if entry.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    form = EntryForm(obj=entry)
    return render_template('entry.html', entry=entry, form=form)

@app.route('/entry/<int:entry_id>/edit', methods=['POST'])
@login_required
def edit_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    if entry.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    form = EntryForm()
    if form.validate_on_submit():
        entry.title = form.title.data
        entry.content = form.content.data
        entry.mood = form.mood.data
        db.session.commit()
        flash('Entry updated successfully!', 'success')
    return redirect(url_for('view_entry', entry_id=entry.id))

@app.route('/search')
@login_required
def search_entries():
    query = request.args.get('q', '')
    mood = request.args.get('mood', '')
    date = request.args.get('date', '')
    
    entries = Entry.query.filter_by(user_id=current_user.id)
    
    if query:
        entries = entries.filter(Entry.title.contains(query))
    if mood:
        entries = entries.filter_by(mood=mood)
    if date:
        try:
            search_date = datetime.strptime(date, '%Y-%m-%d')
            entries = entries.filter(db.func.date(Entry.date) == search_date.date())
        except ValueError:
            flash('Invalid date format', 'error')
    
    entries = entries.order_by(Entry.date.desc()).all()
    return render_template('dashboard.html', entries=entries, form=EntryForm())

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)