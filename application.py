import os

from flask import Flask, session, render_template, request, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home", methods=["POST"])
def home():
    #Get the Form information
    userName = request.form.get("userName")
    print(userName)
    password = request.form.get("password")
    print(password)
    #Check if User is present in Database
    if db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": userName, "password": password}).rowcount == 0:
        flash("UserName is not Found." ,"danger")
        return render_template("signup.html")
    return "Project 1: TODO"

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/success", methods=["POST"])
def success():
    #Get the Form information
    username = request.form.get("user_name")
    if db.execute("SELECT * from users WHERE username = :username", {"username": username}).rowcount != 0:
        return render_template("error.html", message="User Name already exist.")
    try:
        password = str(request.form.get("password_confirmation"))
    except ValueError:
        return render_template("error.html", message="Invalid password.")
    try:
        firstName = str(request.form.get("first_name"))
    except ValueError:
        return render_template("error.html", message="Invalid firstName.")
    try:
        lastName = str(request.form.get("last_name"))
    except ValueError:
        return render_template("error.html", message="Invalid lastName.")
    try:
        email = str(request.form.get("email"))
    except ValueError:
        return render_template("error.html", message="Invalid email.")
    print(firstName)
    print(lastName)
    print(email)
    print((db.execute("SELECT * from users")).rowcount)
    db.execute("INSERT INTO users (username, firstName, lastName, email, password) VALUES (:username, :firstName, :lastName, :email, :password)", {"username": username, "firstName": firstName, "lastName": lastName, "email": email, "password": password})
    db.commit()
    return render_template("success.html")