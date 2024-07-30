#!/usr/bin/env python3
"""
Flask app
"""
from flask import Flask, request, g, render_template
from flask_babel import Babel, _
import pytz
from datetime import datetime
from pytz.exceptions import UnknownTimeZoneError

app = Flask(__name__)
babel = Babel(app)

class Config:
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(Config)

# Mock user data
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user():
    user_id = request.args.get('login_as')
    if user_id and int(user_id) in users:
        return users[int(user_id)]
    return None

@app.before_request
def before_request():
    g.user = get_user()

@babel.localeselector
def get_locale():
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@babel.timezoneselector
def get_timezone():
    timezone = request.args.get('timezone')
    if timezone:
        try:
            return pytz.timezone(timezone)
        except UnknownTimeZoneError:
            pass
    if g.user:
        user_timezone = g.user.get('timezone')
        if user_timezone:
            try:
                return pytz.timezone(user_timezone)
            except UnknownTimeZoneError:
                pass
    return app.config['BABEL_DEFAULT_TIMEZONE']

@app.route('/')
def index():
    current_time = datetime.now(pytz.timezone(get_timezone()))
    formatted_time = current_time.strftime("%b %d, %Y, %I:%M:%S %p")
    return render_template('index.html', current_time=formatted_time)

if __name__ == "__main__":
    app.run(debug=True)

