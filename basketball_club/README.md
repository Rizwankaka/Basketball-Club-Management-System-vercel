# Basketball Club Information System

A web-based application for managing basketball club information, including player details and match statistics.

## Features

- User Authentication (Login/Signup)
- Player Management
  - Add new players with comprehensive details
  - View all players and their information
- Match Statistics
  - Record match statistics for each player
  - Track minutes played, points scored, rebounds, and assists

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd basketball_club
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Create a new account using the Sign Up page
2. Log in with your credentials
3. Use the dashboard to:
   - View all registered players
   - Add new players
   - Record match statistics

## Technologies Used

- Flask (Python web framework)
- SQLAlchemy (Database ORM)
- Flask-Login (User authentication)
- Bootstrap 5 (Frontend styling)
- SQLite (Database)

## Project Structure

```
basketball_club/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── templates/         # HTML templates
    ├── base.html
    ├── index.html
    ├── login.html
    ├── signup.html
    ├── dashboard.html
    ├── add_player.html
    └── add_match_statistic.html
```
