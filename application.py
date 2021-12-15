import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, json
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import requests
from yelp import getMeYelp, getLocation

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///eatYourMood.db")

# Creating list of possible moods
moodList = ["--", "Ecstatic", "Romantic", "Gloomy", "Angry", "Tired", "Cheery", "Tipsy", "Rich"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", moodList=moodList)
    else:

        if request.form.get("moodSelect"):
            mood = request.form.get("moodSelect")
        elif request.form.get("moodInput"):
            mood = request.form.get("moodInput")

        moodToTerm = {
            "Ecstatic": ["brunch", "french food"],
            "Romantic": ["italian", "dessert"],
            "Gloomy": ["comfort food", "tex-mex"],
            "Angry": ["ice cream", "bubble tea"],
            "Tired": ["coffee", "tea"],
            "Cheery": ["drinks"],
            "Tipsy": ["pizza",  "fried food"],
            "Rich": ["sushi", "lobster", "caviar"]
        }

        #===================================
        # Get location based on lat, long
        #print("Latitude:" + request.form.get("lat"))
        print(request.form)

        if request.form.get("lat"):
            session["lat"] = float(request.form.get("lat"))
            session["long"] = float(request.form.get("long"))


        city, postalCode = getLocation(lat=session["lat"], long=session["long"])

        #==========================================================
        # Connect to yelp api and get business information

        yelpDataList = []
        termList = moodToTerm[mood]
        for term in termList:
            yelpDataList.extend(getMeYelp(term=term, postalCode=postalCode))


        yelpDataList = [dict(t) for t in {tuple(d.items()) for d in yelpDataList}]

        #==========================================================
        isLoggedIn = False
        if "user_id" in session:
            isLoggedIn = True


        businessName = request.form.get("businessName")
        location = request.form.get("location")
        phone = request.form.get("phone")
        url = request.form.get("url")
        dbAction = request.form.get("dbAction")
        if businessName:
            if isLoggedIn == True:
                if dbAction == "add":
                    db.execute("INSERT INTO favorites (user_id, favoriteBusiness, location, phone, url) VALUES(:userId, :businessName, :location, :phone, :url)",
                    userId = session["user_id"], businessName = businessName, location = location, phone = phone, url = url)
                else:
                    db.execute("DELETE FROM favorites WHERE user_id = :userId and favoriteBusiness = :businessName",
                    userId = session["user_id"], businessName = businessName)

        if isLoggedIn == True:
            favList = []
            row = db.execute("SELECT favoriteBusiness FROM favorites WHERE user_id = :userId",
            userId = session["user_id"])

            for value in row:
                favList.append(value["favoriteBusiness"])

            for business in yelpDataList:
                if business["name"] in favList:
                    business["fav"] = True

        #==== Update Yelp DataList Fav to true based on the database content===


        #==========================================================
        yelpDataList = sorted(yelpDataList, key = lambda i: (i["distance"], i["name"]))
        return render_template("index.html",
                               yelpDataList = yelpDataList,
                               selectedMood=mood,
                               moodList=moodList,
                               cuisineList=termList,
                               isLoggedIn=isLoggedIn)






@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    if "user_id" in session:
        del session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return render_template("index.html", moodList=moodList)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    del session["user_id"]

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Assign variable names to form requests
        regUsername = request.form.get("username")
        regPassword = request.form.get("password")
        regConfirmP = request.form.get("confirmation")

        # Ensure username was submitted
        if not regUsername:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not regPassword:
            return apology("must provide password", 403)

        # Ensure confirm password was submitted
        elif not regConfirmP:
            return apology("must confirm password", 403)

        # Ensure passwords match
        elif regPassword != regConfirmP:
            return apology("passwords do not match", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=regUsername)

        # Ensure username does not already exist
        if len(rows) != 0:
            return apology("Username already exists", 403)

        # Insert the username into users
        db.execute("INSERT INTO users(username, hash) VALUES(:username, :hash)",
        username=regUsername, hash=generate_password_hash(regPassword))

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/favorites")
@login_required
def favorites():
    favList = db.execute("SELECT favoriteBusiness, location, phone, url FROM favorites WHERE user_id = :userId",
                userId = session["user_id"])

    return render_template("favorites.html", favList=favList)


@app.route("/myHome",methods=["POST", "GET"])
@login_required
def myHome():
    if request.method == "POST":

        if request.form.get("newBudget"):
            myBudget = request.form.get("newBudget")
            print(myBudget)

            db.execute("UPDATE users SET budget = :myBudget WHERE id = :userId",
            myBudget = myBudget, userId = session["user_id"])

        if request.form.get("businessName"):
            businessName = request.form.get("businessName")
            date = request.form.get("date")
            expense = request.form.get("expense")

            db.execute("INSERT INTO transactions(user_id, businessName, expense, purchase_date) VALUES(:userId, :businessName, :expense, :date)" ,
            userId = session["user_id"], businessName = businessName, date = date, expense = expense)



        print(3)

    row = db.execute("SELECT budget FROM users WHERE id = :userId",
          userId = session["user_id"])
    myBudget = row[0]["budget"]

    expenseRow = db.execute("SELECT businessName, expense, purchase_date FROM transactions WHERE user_id = :userId ORDER BY purchase_date DESC",
        userId = session["user_id"])
    myExpense = 0
    for expense in expenseRow:
        myExpense = myExpense + float(expense["expense"])

    return render_template("myHome.html", myBudget=myBudget, myExpense=myExpense, expenseRow=expenseRow[0:5])

@app.route("/history")
@login_required
def history():
    expenseList = db.execute("SELECT businessName, expense, purchase_date FROM transactions WHERE user_id = :userId ORDER BY purchase_date DESC",
        userId = session["user_id"])

    return render_template("history.html", expenseList=expenseList)