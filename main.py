from flask import Flask, render_template, g
import sqlite3


app = Flask(__name__)


# get db function (creates connection, etc.)
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('classical.db')
        db.row_factory = sqlite3.Row  # allows dictionary access
        db.commit()
    return db


@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# my home page
@app.route("/")
def home():
    db = get_db()
    cur = db.execute("""
    SELECT Artwork.art_name,
    Artwork.type,
    Artwork.years,
    Artwork.image,
    Century.century,
    Century.time_period,
    FoundLocation.found_location,
    CurrentLocation.current_location
    FROM Artwork
    JOIN Century ON Artwork.century_id=Century.id
    JOIN FoundLocation ON Artwork.FL_id=FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id= CurrentLocation.id;
    """)
    art = cur.fetchall()
    return render_template("home.html", title="Home", art=art)


# Might delete later as kinda the same as the gallery
@app.route('/all_artworks')
def all_artworks():
    db = get_db()
    cur = db.execute("""
    SELECT
        Artwork.art_name,
        Artwork.type,
        FoundLocation.found_location,
        CurrentLocation.current_location,
        GROUP_CONCAT(Person.name || ' (' || Person.role || ')', ', ') AS people,
        Century.century,
        Century.time_period
    FROM Artwork
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    JOIN ArtworkPerson ON Artwork.id = ArtworkPerson.aid
    JOIN Person ON ArtworkPerson.pid = Person.id
    JOIN Century ON Artwork.century_id = Century.id
    GROUP BY Artwork.id
""")
    art = cur.fetchall()
    return render_template("all_art.html", title="All Art", art=art)


# My location page
@app.route('/location')
def location():
    db = get_db()
    # Just dumping my location data right now
    cur = db.execute("""
    SELECT
    Artwork.art_name,
    Artwork.type,
    FoundLocation.found_location,
    CurrentLocation.current_location
    FROM Artwork
    JOIN FoundLocation ON Artwork.FL_id=FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id= CurrentLocation.id;
    """)
    art = cur.fetchall()
    return render_template("locations.html", title="Locations", art=art)


# My time period page
@app.route('/time_period')
def time_period():
    db = get_db()
    # Just dumping my time_period data right now
    cur = db.execute("""
    SELECT
    Artwork.art_name,
    Artwork.type,
    Artwork.years,
    Century.century,
    Century.time_period
    FROM Artwork
    JOIN Century ON Artwork.century_id=Century.id;
    """)
    art = cur.fetchall()
    return render_template("time_period.html", title="Time Period", art=art)


# Error 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html"), 404


if __name__ == '__main__':
    # TAKE THIS BIT OUT BEFORE SUMBIT
    app.run(debug=True)
