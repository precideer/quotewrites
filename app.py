import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///quotewrites.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Show homepage"""

    # Check if user is logged in
    if session.get("user_id"):
        
        # Redirect to prompt page
        return redirect("/prompt")
    else:
        
        # Show homepage
        return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (by submitting a form)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check whether username was submitted
        if not username:
            return apology("must provide username")

        # Check whether password was submitted
        elif not password:
            return apology("must provide password")
        
        # Check whether password was confirmed
        elif not confirmation:
            return apology("must provide password confirmation")

        # Check whether password and password confirmation match
        elif password != confirmation:
            return apology("passwords must match")

        # Check whether username already exists
        if db.execute("SELECT * FROM users WHERE username = ?", username):
            return apology("username already exists")

        # Hash password to store in database
        hash = generate_password_hash(password)

        # Insert user information into users database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        
        # Remember which user has logged in
        user_id = db.execute("SELECT id FROM users WHERE username = ?", username)
        session["user_id"] = user_id[0]["id"]

        # Redirect user to homepage
        return redirect("/")

    # User reached route via GET (by clicking a link or through redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    session.clear()

    # User reached route via POST (by submitting a form)
    if request.method == "POST":

        # Check whether username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Check whether password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Check whether log in credentials
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to homepage
        return redirect("/")

    # User reached route via GET (by clicking on a a link or through redirect)
    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    """Log user out"""

    session.clear()
    return redirect("/")


@app.route("/prompt", methods=["GET", "POST"])
@login_required
def prompt():
    """Show prompt page with randomly chosen quote"""

    # Query database for random quote
    row = db.execute("SELECT * FROM quotes WHERE id NOT IN (SELECT quote_id FROM quotewrites WHERE user_id = ?) ORDER BY RANDOM() LIMIT 1", session["user_id"])

    # Get quote information
    if row:
        quote = row[0]["quote"]
        author = row[0]["author"]
        title = row[0]["title"]
        quote_id = row[0]["id"]
    else:
        return apology("no quotes available")

    # Render propt page with randomly chosen quote
    return render_template("prompt.html", quote=quote, author=author, title=title, quote_id=quote_id)


@app.route("/bookmark", methods=["POST"])
def bookmark():
    """Save a prompt"""

    quote_id = request.form.get("quote_id")
    quotewrite = request.form.get("quotewrite")

    # Insert a new quotewrite, or update an old quotewrite in the database
    db.execute("INSERT INTO quotewrites (user_id, quote_id, quotewrite) VALUES (:user_id, :quote_id, :quotewrite) ON CONFLICT (user_id, quote_id) DO UPDATE SET quotewrite = :quotewrite", user_id=session["user_id"], quote_id=quote_id, quotewrite=quotewrite)

    return redirect("/prompt")


@app.route("/write", methods=["GET", "POST"])
def write():
    """Write a Quotewrite"""

    # User reached route via POST (by submitting a form)
    if request.method == "POST":

        # Variables
        quote_id = request.form.get("quote_id")
        quotewrite = request.form.get("quotewrite")

        # Check whether input is valid
        if not quote_id or not quotewrite:
            return apology("missing response")

        # Insert a new quotewrite, or update an old quotewrite in the database
        db.execute("INSERT INTO quotewrites (user_id, quote_id, quotewrite) VALUES (:user_id, :quote_id, :quotewrite) ON CONFLICT (user_id, quote_id) DO UPDATE SET quotewrite = :quotewrite", user_id=session["user_id"], quote_id=quote_id, quotewrite=quotewrite)

        # Redirect to My Quotewrites
        return redirect("/my_quotewrites")

    # User reached route via GET (by clicking on a link or through redirect)
    else:
        quote_id = request.args.get("quote_id")

        # Get quote information from database
        quote = db.execute("SELECT * FROM quotes WHERE id = ?", quote_id)

        # Check wheher quote is valid
        if not quote:
            return apology("quote not found")

        # Get existing quotewrite, if applicable
        quotewrite = db.execute("SELECT quotewrite FROM quotewrites WHERE user_id = ? AND quote_id = ?", session["user_id"], quote_id)
        
        # Render Write page
        return render_template("write.html", quote=quote[0], quotewrite=quotewrite[0] if quotewrite else None)


@app.route("/my_quotewrites", methods=["GET"])
@login_required
def my_quotewrites():
    """Desplay main dashboard of bookmarked prompts and quotewrites """

    # Get bookmarked quote prompts
    bookmarks = db.execute("SELECT * FROM quotewrites JOIN quotes ON quotewrites.quote_id = quotes.id WHERE user_id = ? AND quotewrite IS NULL ORDER BY created_at DESC;", session["user_id"])

    # Get started/completed quotewrites
    quotewrites = db.execute("SELECT * FROM quotewrites JOIN quotes ON quotewrites.quote_id = quotes.id WHERE user_id = ? AND quotewrite IS NOT NULL ORDER BY created_at DESC;", session["user_id"])
    
    # Render dashboard
    return render_template("my_quotewrites.html", bookmarks=bookmarks, quotewrites=quotewrites)