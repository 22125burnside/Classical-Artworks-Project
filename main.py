from flask import Flask, render_template, g, abort
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
    # Top 20 most popular artworks/architecture (might change later)
    featured = (20, 15, 14, 4, 5, 40, 7, 6, 49, 2, 3,
                47, 46, 26, 27, 16, 8, 17, 21, 19)
    placeholders = ','.join('?' for _ in featured)
    query = f"""
    SELECT
    Artwork.id,
    Artwork.art_name,
    Artwork.type,
    Artwork.years,
    Century.century,
    Century.time_period,
    FoundLocation.found_location,
    CurrentLocation.current_location
    FROM Artwork
    JOIN Century ON Artwork.century_id = Century.id
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    WHERE Artwork.id IN ({placeholders})
    ORDER BY Artwork.art_name ASC;
    """
    cur = db.execute(query, featured)
    art = cur.fetchall()
    return render_template("home.html", title="Home", art=art)


# Displays all the artworks
@app.route('/all_artworks')
def all_artworks():
    db = get_db()
    cur = db.execute("""
    SELECT
    Artwork.id,
    Artwork.art_name,
    Artwork.type,
    Artwork.years,
    FoundLocation.found_location,
    CurrentLocation.current_location,
    Century.century,
    Century.time_period
    FROM Artwork
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    JOIN Century ON Artwork.century_id = Century.id
    GROUP BY Artwork.id
""")
    art = cur.fetchall()
    return render_template("all_art.html", title="All Art", art=art)


# My location page
@app.route('/location')
def location():
    db = get_db()
    cur = db.execute("""
        SELECT id, found_location
        FROM FoundLocation
        ORDER BY found_location ASC
    """)
    found_locations = cur.fetchall()
    return render_template("locations.html", title="Locations", found_locations=found_locations)


# All the seperate locations (found)
@app.route('/locations/<int:id>')
def separate_locations(id):
    db = get_db()
    cursor = db.execute("""
        SELECT *
        FROM Artwork
        JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
        WHERE FoundLocation.id = ?
    """, (id,))
    # fetching all my artworks that are in that location
    artworks = cursor.fetchall()
    if artworks is None:
        abort(404)
    location_name = artworks[0]['found_location']
    return render_template('seperate_location.html', art=artworks, location_name=location_name)


# My time period page
@app.route('/time_period')
def time_period():
    return render_template("time_period.html", title="Time Period")


# Archaic period page
@app.route('/archaic_period')
def archaic_period():
    db = get_db()
    cur = db.execute("""
    SELECT
    Artwork.id,
    Artwork.art_name,
    Artwork.type,
    Artwork.years,
    Century.century,
    Century.time_period,
    FoundLocation.found_location,
    CurrentLocation.current_location
    FROM Artwork
    JOIN Century ON Artwork.century_id=Century.id
    JOIN FoundLocation ON Artwork.FL_id=FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id= CurrentLocation.id
    WHERE Century.time_period = 'Archaic Period'
    ORDER BY years DESC;
    """)
    art = cur.fetchall()
    return render_template('archaic.html', title="Archaic Period Artwork", art=art)


# Hellenistic period page
@app.route('/hellenistic_period')
def hellenistic_period():
    db = get_db()
    cur = db.execute("""
    SELECT
    Artwork.id,
    Artwork.art_name,
    Artwork.type,
    Artwork.years,
    Century.century,
    Century.time_period,
    FoundLocation.found_location,
    CurrentLocation.current_location
    FROM Artwork
    JOIN Century ON Artwork.century_id=Century.id
    JOIN FoundLocation ON Artwork.FL_id=FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id= CurrentLocation.id
    WHERE Century.time_period = 'Hellenistic Period'
    ORDER BY years DESC;
    """)
    art = cur.fetchall()
    return render_template('hellenistic.html', title="Hellenistic Period Artwork", art=art)


# Roman Art period page
@app.route('/roman_period')
def roman_period():
    db = get_db()
    cur = db.execute("""
    SELECT
    Artwork.id,
    Artwork.art_name,
    Artwork.type,
    Artwork.years,
    Century.century,
    Century.time_period,
    FoundLocation.found_location,
    CurrentLocation.current_location
    FROM Artwork
    JOIN Century ON Artwork.century_id=Century.id
    JOIN FoundLocation ON Artwork.FL_id=FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id= CurrentLocation.id
    WHERE Century.time_period = 'Roman Art'
    ORDER BY years DESC;
    """)
    art = cur.fetchall()
    return render_template('Roman_art.html', title="Roman Art Period Artwork", art=art)


# Classical art period page
@app.route('/classical_period')
def classical_period():
    db = get_db()
    cur = db.execute("""
    SELECT
    Artwork.id,
    Artwork.art_name,
    Artwork.type,
    Artwork.years,
    Century.century,
    Century.time_period,
    FoundLocation.found_location,
    CurrentLocation.current_location
    FROM Artwork
    JOIN Century ON Artwork.century_id=Century.id
    JOIN FoundLocation ON Artwork.FL_id=FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id= CurrentLocation.id
    WHERE Century.time_period = 'Classical Period'
    ORDER BY years DESC;
    """)
    art = cur.fetchall()
    return render_template('classical_art.html', title="Classical Art Period Artwork", art=art)


# Page for all the characters
@app.route('/characters')
def characters():
    db = get_db()
    cur = db.execute("""
    SELECT
    Artwork.id,
    Person.id AS person_id,
    Person.name,
    Person.role,
    GROUP_CONCAT(Artwork.art_name, ', ') AS artworks
    FROM Person
    JOIN ArtworkPerson ON Person.id = ArtworkPerson.pid
    JOIN Artwork ON Artwork.id = ArtworkPerson.aid
    GROUP BY Person.id
    ORDER BY Person.name ASC;
    """)
    people = cur.fetchall()
    return render_template('character.html', title="People", people=people)


@app.route('/frescoes')
def frescoes():
    db = get_db()
    cur = db.execute("""
    SELECT
    Artwork.id,
    Artwork.art_name,
    Artwork.type,
    Artwork.years,
    FoundLocation.found_location,
    CurrentLocation.current_location,
    Century.century,
    Century.time_period
    FROM Artwork
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    JOIN Century ON Artwork.century_id = Century.id
    WHERE Artwork.type = 'Fresco'
    """)
    art = cur.fetchall()
    return render_template("fresco.html", title="Frescoes", art=art)


@app.route('/vases')
def vases():
    db = get_db()
    cur = db.execute("""
    SELECT
    Artwork.id,
    Artwork.art_name,
    Artwork.type,
    Artwork.years,
    FoundLocation.found_location,
    CurrentLocation.current_location,
    Century.century,
    Century.time_period
    FROM Artwork
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    JOIN Century ON Artwork.century_id = Century.id
    WHERE Artwork.type = 'Vase'
    """)
    art = cur.fetchall()
    return render_template("vase.html", title="Vases", art=art)


@app.route('/sculptures')
def sculptures():
    db = get_db()
    cur = db.execute("""
    SELECT
    Artwork.id,
    Artwork.art_name,
    Artwork.type,
    Artwork.years,
    FoundLocation.found_location,
    CurrentLocation.current_location,
    Century.century,
    Century.time_period
    FROM Artwork
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    JOIN Century ON Artwork.century_id = Century.id
    WHERE Artwork.type = 'Sculpture'
    """)
    art = cur.fetchall()
    return render_template("sculpture.html", title="Sculptures", art=art)


@app.route('/architecture')
def architect():
    db = get_db()
    cur = db.execute("""
    SELECT
    Artwork.id,
    Artwork.art_name,
    Artwork.type,
    Artwork.years,
    FoundLocation.found_location,
    CurrentLocation.current_location,
    Century.century,
    Century.time_period
    FROM Artwork
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    JOIN Century ON Artwork.century_id = Century.id
    WHERE Artwork.type = 'Architecture'
    """)
    art = cur.fetchall()
    return render_template("architect.html", title="Architecture", art=art)


@app.route('/reliefs')
def reliefs():
    db = get_db()
    cur = db.execute("""
    SELECT
    Artwork.id,
    Artwork.art_name,
    Artwork.type,
    Artwork.years,
    FoundLocation.found_location,
    CurrentLocation.current_location,
    Century.century,
    Century.time_period
    FROM Artwork
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    JOIN Century ON Artwork.century_id = Century.id
    WHERE Artwork.type = 'Relief'
    """)
    art = cur.fetchall()
    return render_template("relief.html", title="Reliefs", art=art)


@app.route('/mosaics')
def mosaics():
    db = get_db()
    cur = db.execute("""
    SELECT
    Artwork.id,
    Artwork.art_name,
    Artwork.type,
    Artwork.years,
    FoundLocation.found_location,
    CurrentLocation.current_location,
    Century.century,
    Century.time_period
    FROM Artwork
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    JOIN Century ON Artwork.century_id = Century.id
    WHERE Artwork.type = 'Mosaic'
    """)
    art = cur.fetchall()
    return render_template("mosaics.html", title="Mosaics", art=art)


@app.route('/jewellery')
def jewellery():
    db = get_db()
    cur = db.execute("""
    SELECT
    Artwork.id,
    Artwork.art_name,
    Artwork.type,
    Artwork.years,
    FoundLocation.found_location,
    CurrentLocation.current_location,
    Century.century,
    Century.time_period
    FROM Artwork
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    JOIN Century ON Artwork.century_id = Century.id
    WHERE Artwork.type = 'Jewellery'
    """)
    art = cur.fetchall()
    return render_template("jewellery.html", title="Jewellery", art=art)


# All the seperate individual pages for each artwork
@app.route('/seperate_artworks/<int:id>')
def seperate_artworks(id):
    db = get_db()
    cursor = db.execute("""
    SELECT *
    FROM Artwork
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    JOIN Century ON Artwork.century_id = Century.id
    JOIN ArtworkPerson ON Artwork.id = ArtworkPerson.aid
    JOIN Person ON ArtworkPerson.pid = Person.id
    WHERE Artwork.id = ?""", (id,))
    # Only fetching one piece of info (the artwork)
    row = cursor.fetchone()
    if row is None:
        abort(404)
    return render_template('seperate.html', title=row["art_name"], row=row)


# Error 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html"), 404


if __name__ == '__main__':
    # TAKE THIS BIT OUT BEFORE SUMBIT
    app.run(debug=True)
