import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
import logging
logging.basicConfig(level=logging.DEBUG)

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "GET":
        listofdict = db.execute("SELECT symbol,SUM(no_of_shares) AS no_of_shares ,cash FROM users JOIN entry ON users.id = entry.user_id WHERE user_id = ? GROUP BY symbol", session.get("user_id", None))
        holdingvalue = 0
        print(listofdict)
        if(listofdict == []):
            return apology("No purchases yet", 200)
        else:
            for dict in listofdict:
                dict["currentprice"] = lookup(dict.get('symbol')).get("price")
                dict["currentvalue"] = dict.get('no_of_shares') * dict.get('currentprice')
                holdingvalue = holdingvalue + lookup(dict.get('symbol')).get("price") * dict.get('no_of_shares')
            grandtotal = dict.get('cash') + holdingvalue
            cash = dict.get('cash')
            return render_template("portfolio.html", listofdict = listofdict, grandtotal = grandtotal, cash = cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        number = request.form.get("shares")
        if lookup(symbol) == None:
            return apology("please enter a valid symbol")
        elif number.isdigit() == False :
            return apology("please enter a positive integer for number of shares")
        price = lookup(symbol).get("price")
        value = price*int(number)
        cashleft = db.execute("SELECT cash FROM users WHERE id = ?", session.get("user_id", None))
        remainingcash = cashleft[0]["cash"]
        newremainingcash = remainingcash - value
        if value > remainingcash:
            return apology("not enough cash")
        else:
             db.execute("UPDATE users SET cash = ? WHERE id = ?", newremainingcash, session.get("user_id", None))
             db.execute("INSERT INTO entry (user_id, symbol, no_of_shares, price) VALUES (?,?,?,?)", session.get("user_id", None), symbol, number, price)
             return redirect("/")
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    if request.method == "GET":
        listofdict = db.execute("SELECT time, symbol, no_of_shares, price FROM entry WHERE user_id = ?", session.get("user_id", None))
        for dict in listofdict:
            print(dict)
            if dict["no_of_shares"] > 0:
                dict["bs"] = "buy"
            else:
                dict["bs"] = "sell"
                dict["no_of_shares"] = -dict["no_of_shares"]
        return render_template("history.html", listofdict=listofdict)
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        result = lookup(symbol)
        if result == None:
            return apology("No such symbol")
        price = usd(result["price"])

    return render_template("quoted.html", symbol=symbol, price=price)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        unique = db.execute("SELECT * FROM users WHERE username = ?", username)
        if password != confirmation:
            return apology("password doesnt match confirmation")
        if username and password:
            if not unique:
                db.execute("INSERT INTO users ('username', 'hash') VALUES (?,?)", username, generate_password_hash(password))
                return redirect("/login")
            else:
                return apology("please select a unique username")
        else:
            return apology("please enter username and/or password")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        options = db.execute("SELECT symbol FROM entry WHERE user_id = ? GROUP BY symbol HAVING SUM(no_of_shares) > 0 ", session.get("user_id", None))
        return render_template("sell.html", options = options)
    else:
        symbol = request.form.get("symbol")
        number = request.form.get("shares")
        if number.isdigit() == False:
            return apology("Please enter a valid number of shares")
        number = int(number)
        sellnumber = -number
        price = lookup(symbol).get("price")
        value = price*number
        cash = int(db.execute("SELECT cash FROM users WHERE id = ?", session.get("user_id", None))[0].get("cash"))
        cash = cash + value
        avail = int(db.execute ("SELECT SUM(no_of_shares) AS avail FROM entry WHERE user_id = ? AND symbol = ? GROUP BY symbol", session.get("user_id", None), symbol)[0].get("avail"))
        if not symbol:
            return apology("please select a symbol")
        elif not number:
            return apology("please input a valid number")
        elif avail < number:
            return apology("you do not own that many shares")
        else:

            db.execute("INSERT INTO entry (user_id, symbol, no_of_shares, price) VALUES (?,?,?,?)", session.get("user_id", None), symbol, sellnumber, price)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session.get("user_id", None))
            return redirect("/")
