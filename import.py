import os
import csv

from flask import Flask, render_template, request
from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

engine = create_engine(os.getenv("DATABASE_URL"))
database = scoped_session(sessionmaker(bind=engine))

def main():
    db.create_all()
    f = open("books.csv")
    reader = csv.reader(f)
    #skip the header
    next(reader)
    for isbn, title, author, year in reader:
        database.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
               {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Adding to DB -- isbn - {isbn}| book - {title}| Author - {author}| published - {year} ")
    database.commit()


if __name__ == "__main__":
    with app.app_context():
        main()
