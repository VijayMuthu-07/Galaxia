import os
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup_nasa, lookup_spacex, lookup_articles

# Configure application
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder if not exists

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///media.db")

db.execute('''CREATE TABLE IF NOT EXISTS uploads (
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              text TEXT, 
              photo_path TEXT, 
              video_path TEXT)''')

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username/email was submitted
        if not request.form.get("username"):
            return apology("must provide username or email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if(rows == []):
            rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["u_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Ensure username/email was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("email"):
            return apology("must provide email", 400)

        # Ensure password/ verification was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("verification"):
            return apology("must re-type password for verification", 400)

        if request.form.get("verification") != request.form.get("password"):
            return apology("retyped password didn't match", 400)

        # Query database for username
        try:
            db.execute("INSERT INTO users(username, email, hash) VALUES(?, ?, ?)",request.form.get("username"), request.form.get("email"), generate_password_hash(request.form.get("password")))
        except ValueError:
            return apology("username or email already taken", 400)
        
        db.execute("INSERT INTO userdata(username, type, data, pst) VALUES(?, ?, ?, ?)", request.form.get("username"), "bio", "", None)

        # Redirect user to home page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/settings", methods=["GET"])
@login_required
def settings():
    return render_template("settings.html")

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    session.clear()
    return redirect("/login")

@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    if request.method == "POST":
        if not request.form.get("oldpassword"):
            return apology("must provide old password", 400)
        elif not request.form.get("newpassword"):
            return apology("must provide new password", 400)
        elif not request.form.get("confirmation"):
            return apology("must re-type password for verification", 400)
        
        rows = db.execute("SELECT * FROM users WHERE u_id = ?", session["user_id"])
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("oldpassword")):
            return apology("invalid username and/or password", 403)
        
        if request.form.get("confirmation") != request.form.get("newpassword"):
            return apology("retyped password didn't match", 400)

        # Query for database
        try:
            db.execute("UPDATE users SET hash = ? WHERE u_id = ?", generate_password_hash(request.form.get("newpassword")), session["user_id"])
        except Exception:
            return apology("Something went wrong...", 400)
        
        session.clear()
        return redirect("/login")

    else:
        return render_template("change.html")
    
@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "POST":
        if not request.form.get("password"):
            return apology("must provide yor password")
        
        rows = db.execute("SELECT * FROM users WHERE u_id = ?", session["user_id"])
        username = rows[0]["username"]

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        try:
            db.execute("DELETE FROM users WHERE u_id = ?", session["user_id"])
            db.execute("DELETE FROM userdata WHERE username = ?", username)
        except Exception:
            return apology("Something went wrong...", 403)
        
        session.clear()
        return redirect("/login")
    else:
        return render_template("delete.html")

@app.route("/news", methods=["GET"])
@login_required
def news():
    apod_data = lookup_nasa()
    spacex_data = lookup_spacex()
    space_news_data = lookup_articles()

    return render_template("news.html", apod=apod_data, spacex=spacex_data, news=space_news_data)

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    data = db.execute("SELECT * FROM users WHERE u_id = ?", session["user_id"])
    username = data[0]["username"]

    if request.method == "POST":
        bio = request.form.get("bio", "")
        db.execute("UPDATE userdata SET data = ? WHERE username = ? AND type = ?", bio, username, "bio")

        return redirect("/profile")
           
    else:
        rows = db.execute("SELECT * FROM userdata WHERE username = ? AND type = ?", username, "bio")
        bio_data = rows[0]["data"] if rows else ""
        return render_template("profile.html", bio=bio_data, username=username)

@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    data = db.execute("SELECT * FROM users WHERE u_id = ?", session["user_id"])
    username = data[0]["username"]

    if request.method == "POST":
        current_time = datetime.now()

        # Format it in SQL TIMESTAMP format (YYYY-MM-DD HH:MM:SS)
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

        text = request.form.get("chat")
        if not text:
            return redirect("/chat")
        db.execute("INSERT INTO userdata(username, type, data, pst) VALUES(?, ?, ?, ?)", username, "chat", text, formatted_time)
        return redirect("/chat")
    else:
        rows = db.execute("SELECT * FROM userdata WHERE type = ?", "chat")
        return render_template("chat.html", rows=rows, user=username)

@app.route("/feed", methods=["GET", "POST"])
@login_required
def feed():
    if request.method == "POST":
        text = request.form.get("text")  # Get text input

        # Handle photo upload
        photo = request.files.get("photo")
        if not photo:
            return apology("image must be provided", 400)
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
        photo.save(photo_path)
        photo_path = f"static/uploads/{photo.filename}"  # Store relative path in DB

        # Handle video upload
        video = request.files.get("video")
        video_path = None
        if video and video.filename:
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
            video.save(video_path)  # Save video to uploads folder

        # Insert into database using CS50 SQL
        db.execute("INSERT INTO uploads (text, photo_path, video_path) VALUES (?, ?, ?)", 
                   text, photo_path, video_path)

        return redirect("/feed")
    else:
        uploads = db.execute("SELECT * FROM uploads")
        return render_template("feed.html", uploads=uploads)
    