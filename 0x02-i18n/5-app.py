#!/usr/bin/env python3
"""
Flask app with mock user login
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel

app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'

babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user() -> dict:
    """
    Get user from URL parameter 'login_as'.
    """
    user_id = request.args.get('login_as')
    if user_id:
        user_id = int(user_id)
        return users.get(user_id)
    return None

@app.before_request
def before_request() -> None:
    """
    Set user before processing request.
    """
    g.user = get_user()

@app.route('/')
def index() -> str:
    """
    Handle home page.
    """
    return render_template('5-index.html')

if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0", debug=True)
