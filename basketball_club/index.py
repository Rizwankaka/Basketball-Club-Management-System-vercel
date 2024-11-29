from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from urllib.parse import quote

app = Flask(__name__)

# Configure app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database configuration
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Handle special characters in password
    if '@' in database_url:
        prefix, rest = database_url.split('@', 1)
        parts = prefix.split(':')
        if len(parts) >= 3:
            password = quote(parts[2])
            database_url = f"{parts[0]}:{parts[1]}:{password}@{rest}"
    
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    if '?' not in database_url:
        database_url += '?sslmode=require'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basketball_club.db'

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    height = db.Column(db.Float, nullable=False)
    position = db.Column(db.String(20), nullable=False)
    statistics = db.relationship('MatchStatistic', backref='player', lazy=True)

class MatchStatistic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    match_date = db.Column(db.Date, nullable=False)
    minutes_played = db.Column(db.Integer, nullable=False)
    points_scored = db.Column(db.Integer, nullable=False)
    rebounds = db.Column(db.Integer, nullable=False)
    assists = db.Column(db.Integer, nullable=False)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to Basketball Club API"}), 200

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    players = Player.query.all()
    return render_template('dashboard.html', players=players)

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "API is working!"}), 200

# Create tables
with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")

# Vercel handler
def handler(request):
    """Handle requests in Vercel serverless function."""
    if request.method == "POST":
        return app.handle_request()
    
    with app.test_client() as test_client:
        return test_client.get(request.path)
