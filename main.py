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
    # Top 20 most popular artworks/architecture (might change later)
    featured = (20, 15, 14, 4, 5, 40, 7, 6, 49, 2, 3, 47, 46, 26, 27, 16, 8, 17, 21, 19)
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
    # Just dumping my location data right now
    cur = db.execute("""
    SELECT
    Artwork.id,
    Artwork.art_name,
    Artwork.type,
    Artwork.years, 
    FoundLocation.found_location,
    CurrentLocation.current_location
    FROM Artwork
    JOIN FoundLocation ON Artwork.FL_id=FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id= CurrentLocation.id
    ORDER BY CurrentLocation.current_location ASC;
    """)
    art = cur.fetchall()
    # Sort headers by current locations
    locations = sorted(set(row['current_location'] for row in art))
    return render_template("locations.html", title="Locations", art=art, locations=locations)


# My time period page
@app.route('/time_period')
def time_period():
    db = get_db()
    cur = db.execute("""
    SELECT
    Artwork.id,
    Artwork.art_name,
    Artwork.type,
    Artwork.years,
    Century.century,
    Century.time_period
    FROM Artwork
    JOIN Century ON Artwork.century_id=Century.id
    ORDER BY years DESC;
    """)
    art = cur.fetchall()
    # Sort header by time periods 
    time_periods = set(row['time_period'] for row in art)
    return render_template("time_period.html", title="Time Period", art=art, time_periods=time_periods)


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
        return render_template("error.html")
    db.close()
    return render_template('seperate.html', title=row["art_name"], row=row)


# Error 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html"), 404


if __name__ == '__main__':
    # TAKE THIS BIT OUT BEFORE SUMBIT
    app.run(debug=True)
