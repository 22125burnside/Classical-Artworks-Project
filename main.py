from flask import Flask, render_template, g, abort
import sqlite3


app = Flask(__name__)


# Get a database connection, creating one if it doesn't exist
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('classical.db')
        db.row_factory = sqlite3.Row  # allows dictionary access
        db.commit()
    return db


@app.teardown_appcontext
# Close the database at the end of the request
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# home page (shows featured artworks)
@app.route("/")
def home():
    db = get_db()
    # id's for featured artworks
    featured = (20, 15, 14, 4, 5, 40, 7, 6, 49, 2, 3,
                47, 46, 26, 27, 16, 8, 17, 21, 19)
    # Creates a string of ? based on how many featured artworks there are
    placeholders = ','.join('?' for _ in featured)
    # f string allows injection of placeholders
    query = f"""
    SELECT
    Artwork.*, -- grabs everything from artwork table
    Century.century,
    Century.time_period,
    FoundLocation.found_location,
    CurrentLocation.current_location
    FROM Artwork
    -- joining other tables so I can get info
    JOIN Century ON Artwork.century_id = Century.id
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    WHERE Artwork.id IN ({placeholders})
    -- only executes query for featured artworks
    ORDER BY Artwork.art_name ASC;
    """
    cur = db.execute(query, featured)  # execute query
    art = cur.fetchall()
    return render_template("home.html", title="Home", art=art)


# Page displaying all the artworks
@app.route('/all_artworks')
def all_artworks():
    db = get_db()
    cur = db.execute("""
    SELECT
    Artwork.*,
    FoundLocation.found_location,
    CurrentLocation.current_location,
    Century.century,
    Century.time_period
    FROM Artwork
    -- connect neccessary tables
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    JOIN Century ON Artwork.century_id = Century.id
""")
    art = cur.fetchall()
    return render_template("all_art.html", title="All Art", art=art)


# Page listing all current locations
@app.route('/current_location')
def current_location():
    db = get_db()
    # selecting everything from current_location
    cur = db.execute("""
        SELECT *
        FROM CurrentLocation
        ORDER BY current_location ASC;
    """)
    locations = cur.fetchall()
    return render_template(
        'current_location.html',
        title="Current Locations",
        locations=locations)


# Page for individual current location
@app.route('/current_locations/<int:id>')
def current_location_page(id):
    db = get_db()
    cur = db.execute("""
    SELECT *
    FROM Artwork
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN Century ON Artwork.century_id = Century.id
    WHERE CurrentLocation.id = ?
    ORDER BY Artwork.art_name ASC;
    """, (id,))
    art = cur.fetchall()
    if not art:
        abort(404)
    location_name = art[0]['current_location']
    return render_template(
        'sep_current_location.html',
        title=location_name,
        art=art,
        location_name=location_name)


# Page listing all found locations
@app.route('/found_location')
def found_location():
    db = get_db()
    # selecting everything from found_location
    cur = db.execute("""
        SELECT *
        FROM FoundLocation
        ORDER BY found_location ASC;
    """)
    locations = cur.fetchall()
    return render_template(
        'found_location.html',
        title="Found Locations",
        locations=locations)


# Page for found location
@app.route('/found_locations/<int:id>')
def found_location_page(id):
    db = get_db()
    cur = db.execute("""
    SELECT *
    FROM Artwork
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN Century ON Artwork.century_id = Century.id
    WHERE FoundLocation.id = ?
    ORDER BY Artwork.art_name ASC;
    """, (id,))
    art = cur.fetchall()
    if not art:
        abort(404)
    location_name = art[0]['found_location']
    return render_template(
        'sep_found_location.html',
        title=location_name,
        art=art,
        location_name=location_name)


# Page listing time periods and has blurbs for each
@app.route('/time_period')
def time_period():
    return render_template("time_period.html", title="Time Period")


# page for each individual time period page
@app.route('/period/<period_name>')
# period_name changes based on period page asked for
def period_page(period_name):
    db = get_db()
    cur = db.execute("""
    SELECT
    Artwork.*,
    Century.century,
    Century.time_period,
    FoundLocation.found_location,
    CurrentLocation.current_location
    FROM Artwork
    JOIN Century ON Artwork.century_id = Century.id
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    -- ? is a placeholder for period_name
    WHERE Century.time_period = ?
    ORDER BY years DESC;
    """, (period_name,))
    # fetch results that match the query
    art = cur.fetchall()
    if not art:
        # abort if results are empty (will go to error_404 page)
        abort(404)
    return render_template(
        'period.html',
        # Sets title name as the period name
        title=f"{period_name} Artwork",
        art=art)


# Page for all the characters
@app.route('/characters')
def characters():
    db = get_db()
    cur = db.execute("""
    SELECT
    Artwork.id,
    -- so there isn't two values with the same name
    Person.id AS person_id,
    Person.name,
    Person.role,
    -- takes all artworks linked to person and puts in list
    GROUP_CONCAT(Artwork.art_name, ', ') AS artworks
    FROM Person
    JOIN ArtworkPerson ON Person.id = ArtworkPerson.pid
    JOIN Artwork ON Artwork.id = ArtworkPerson.aid
    GROUP BY Person.id
    ORDER BY Person.name ASC;
    """)
    # returns a list of rows that corresponds to each person (no duplicates)
    people = cur.fetchall()
    return render_template(
        'character.html',
        title="People",
        people=people)


# page for each individual type (e.g. fresco)
@app.route('/artworks/<art_type>')
def artwork_types(art_type):
    db = get_db()
    cur = db.execute("""
    SELECT
    -- select certain information
    Artwork.*,
    FoundLocation.found_location,
    CurrentLocation.current_location,
    Century.century,
    Century.time_period
    FROM Artwork
    -- connect to other tables
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    JOIN Century ON Artwork.century_id = Century.id
    WHERE Artwork.type = ? -- filters artwork by type
    """, (art_type.capitalize(),))  # prevents sql injection
    art = cur.fetchall()
    if not art:
        # aborts to error_404 page if no types are found
        abort(404)
    return render_template(
        'artworks.html',
        title=art_type.capitalize(),
        art=art)


# All the seperate individual pages for each artwork
@app.route('/seperate_artworks/<int:id>')
def seperate_artworks(id):
    db = get_db()
    cursor = db.execute("""
    SELECT
    Artwork.*,
    FoundLocation.found_location,
    CurrentLocation.current_location,
    CurrentLocation.region,
    Century.century,
    Century.time_period,
    -- groups all people in a single row
    GROUP_CONCAT(Person.name, ', ') AS people
    FROM Artwork
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    JOIN Century ON Artwork.century_id = Century.id
    LEFT JOIN ArtworkPerson ON Artwork.id = ArtworkPerson.aid
    LEFT JOIN Person ON ArtworkPerson.pid = Person.id
    WHERE Artwork.id = ?
    GROUP BY Artwork.id
    """, (id,))
    art = cursor.fetchone()
    if not art:
        abort(404)
    return render_template('seperate.html', title=art["art_name"], art=art)


# Error 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html"), 404


if __name__ == '__main__':
    # TAKE THIS BIT OUT BEFORE SUMBIT
    app.run(debug=True)
