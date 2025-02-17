import requests

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def lookup_nasa():
    """Look up quote for symbol."""
    # NASA API Key (Replace with your key)
    NASA_API_KEY = "Pe25fS6nmdNeSOSJpIvJW3sPw4Z5sahMQg52PhMT"
    NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"


    """Fetch Astronomy Picture of the Day (APOD) from NASA API."""
    params = {"api_key": NASA_API_KEY}
    response = requests.get(NASA_APOD_URL, params=params)
    return response.json() if response.status_code == 200 else {"error": "Failed to fetch data"}

def lookup_spacex():
    SPACEX_LAUNCHES_URL = "https://api.spacexdata.com/v4/launches/upcoming"
    """Fetch upcoming SpaceX launches."""
    response = requests.get(SPACEX_LAUNCHES_URL)
    
    if response.status_code == 200:
        launches = response.json()
        return launches[:5]  # Get only the first 5 launches
    
    return {"error": "Failed to fetch SpaceX data"}

def lookup_articles():
    """Fetch latest space news with summaries."""
    SPACE_NEWS_URL = "https://api.spaceflightnewsapi.net/v4/articles"
    response = requests.get(SPACE_NEWS_URL)

    if response.status_code == 200:
        return response.json()["results"][:7]  # Limit to 5 articles
    return {"error": "Failed to fetch space news"}
