from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

app = Flask(__name__)

# Configure app for production
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database configuration
if os.environ.get('FLASK_ENV') == 'production':
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Handle special characters in password
        parts = database_url.split('@')
        if len(parts) == 2:
            credentials = parts[0].split(':')
            if len(credentials) == 3:  # postgresql://user:password format
                password = quote_plus(credentials[2])
                database_url = f"{credentials[0]}:{credentials[1]}:{password}@{parts[1]}"
        
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        if 'supabase' in database_url and '?' not in database_url:
            database_url += '?sslmode=require'
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basketball_club.db'

db = SQLAlchemy()
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
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
    matches = db.relationship('MatchStatistic', backref='player', lazy=True)

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

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = User(
            username=request.form['username'],
            email=request.form['email']
        )
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard')
@login_required
def dashboard():
    players = Player.query.all()
    return render_template('dashboard.html', players=players, now=datetime.now().date())

@app.route('/add_player', methods=['GET', 'POST'])
@login_required
def add_player():
    if request.method == 'POST':
        player = Player(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            date_of_birth=datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d'),
            height=float(request.form['height']),
            position=request.form['position']
        )
        db.session.add(player)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_player.html')

@app.route('/add_match_statistic', methods=['GET', 'POST'])
@login_required
def add_match_statistic():
    if request.method == 'POST':
        stat = MatchStatistic(
            player_id=request.form['player_id'],
            match_date=datetime.strptime(request.form['match_date'], '%Y-%m-%d'),
            minutes_played=int(request.form['minutes_played']),
            points_scored=int(request.form['points_scored']),
            rebounds=int(request.form['rebounds']),
            assists=int(request.form['assists'])
        )
        db.session.add(stat)
        db.session.commit()
        return redirect(url_for('dashboard'))
    players = Player.query.all()
    return render_template('add_match_statistic.html', players=players)

@app.route('/team_statistics')
@login_required
def team_statistics():
    # Calculate total games (unique match dates)
    total_games = db.session.query(db.func.count(db.func.distinct(MatchStatistic.match_date))).scalar() or 0

    # Calculate team averages
    avg_stats = db.session.query(
        db.func.avg(MatchStatistic.points_scored).label('avg_points'),
        db.func.avg(MatchStatistic.rebounds).label('avg_rebounds'),
        db.func.avg(MatchStatistic.assists).label('avg_assists')
    ).first()

    # Calculate player statistics
    player_stats = []
    players = Player.query.all()
    
    for player in players:
        stats = db.session.query(
            db.func.count(MatchStatistic.id).label('games_played'),
            db.func.avg(MatchStatistic.points_scored).label('avg_points'),
            db.func.avg(MatchStatistic.rebounds).label('avg_rebounds'),
            db.func.avg(MatchStatistic.assists).label('avg_assists'),
            db.func.avg(MatchStatistic.minutes_played).label('avg_minutes')
        ).filter(MatchStatistic.player_id == player.id).first()

        if stats.games_played > 0:
            player_stats.append({
                'player_name': f"{player.first_name} {player.last_name}",
                'games_played': stats.games_played,
                'avg_points': stats.avg_points or 0,
                'avg_rebounds': stats.avg_rebounds or 0,
                'avg_assists': stats.avg_assists or 0,
                'avg_minutes': stats.avg_minutes or 0
            })

    # Sort players by average points
    player_stats.sort(key=lambda x: x['avg_points'] or 0, reverse=True)

    return render_template('team_statistics.html',
                         total_games=total_games,
                         avg_points=avg_stats.avg_points or 0,
                         avg_rebounds=avg_stats.avg_rebounds or 0,
                         avg_assists=avg_stats.avg_assists or 0,
                         player_stats=player_stats)

@app.route('/test-db')
def test_db():
    try:
        # Try to create all tables
        db.create_all()
        return jsonify({
            "status": "success",
            "message": "Database connection successful",
            "database_url": app.config['SQLALCHEMY_DATABASE_URI'].split('@')[1]  # Only show host part for security
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
