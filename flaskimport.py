from flask import Flask, render_template
import sqlite3


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route('/all_artworks')
def all_artworks():
    conn = sqlite3.connect("classical.db")
    cur = conn.cursor()
    cur.execute("""SELECT Artwork.art_name, Artwork.type,
    FoundLocation.found_location, CurrentLocation.current_location, Person.name,
    Person.role, Century.century, Century.time_period
    FROM Artwork
    JOIN FoundLocation ON Artwork.FL_id=FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id= CurrentLocation.id;
    JOIN ArtworkPerson ON Artwork.id=ArtworkPerson.aid
    JOIN Person ON ArtworkPerson.pid=Person.id
    """)
    art = cur.fetchall()
    conn.close()
    return render_template("all_art.html", art=art)


@app.route('/location')
def location():
    conn = sqlite3.connect("classical.db")
    cur = conn.cursor()
    cur.execute("""SELECT Artwork.art_name, Artwork.type,
    FoundLocation.found_location, CurrentLocation.current_location
    FROM Artwork
    JOIN FoundLocation ON Artwork.FL_id=FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id= CurrentLocation.id;
    """)
    art = cur.fetchall()
    conn.close()
    return render_template("location.html", art=art)


if __name__ == '__main__':
    # TAKE THIS BIT OUT BEFORE SUMBIT
    app.run(debug=True)
