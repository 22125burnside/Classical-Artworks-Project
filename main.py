from flask import Flask, render_template, g, abort
import sqlite3


app = Flask(__name__)


# List of the information in the blurbs (adding into database later)
locations = [
    {"id": 1, "name": "House of Vettii, Pompeii", "details": "A wealthy Roman townhouse that offers a snapshot of elite life in Pompeii before the eruption of Vesuvius.", "region": "Italy"},
    {"id": 2, "name": "Esquiline Hill, Rome", "details": "One of the Seven Hills of Rome, once home to aristocratic houses, gardens, and later imperial palaces.", "region": "Italy"},
    {"id": 3, "name": "Pompeii, Italy", "details": "An ancient Roman city frozen in time after the eruption of Mount Vesuvius in 79 CE.", "region": "Italy"},
    {"id": 4, "name": "Samothrace, Greece", "details": "A small island in the northern Aegean, famed for its Sanctuary of the Great Gods and mystery cult rituals.", "region": "Greece"},
    {"id": 5, "name": "Knidos, Turkey", "details": "An ancient coastal city known for its harbors, temples, and prominence in trade and culture.", "region": "Turkey"},
    {"id": 6, "name": "Villa of Livia, Prima Porta", "details": "A grand Roman villa associated with the family of Emperor Augustus, set in the countryside north of Rome.", "region": "Italy"},
    {"id": 8, "name": "House of Faun, Pompeii", "details": "One of the largest and most luxurious private residences in Pompeii, reflecting elite Roman domestic life.", "region": "Italy"},
    {"id": 9, "name": "Villa of Mysteries, Pompeii", "details": "A villa on the outskirts of Pompeii, celebrated for its size and its enigmatic frescoed rooms.", "region": "Italy"},
    {"id": 10, "name": "House of Dioscuri, Pompeii", "details": "A Roman townhouse noted for its scale and decoration, situated in the heart of Pompeii.", "region": "Italy"},
    {"id": 11, "name": "House of The Tragic Poet, Pompeii", "details": "Known for its mosaics and the famous 'Beware of the Dog' floor inscription.", "region": "Italy"},
    {"id": 12, "name": "Rome, Italy", "details": "The capital of the Roman Empire, home to monumental forums, temples, and imperial art.", "region": "Italy"},
    {"id": 13, "name": "Athens, Greece", "details": "The heart of Classical Greece, celebrated for the Acropolis and artistic innovation.", "region": "Greece"},
    {"id": 14, "name": "Epidaurus, Greece", "details": "A sanctuary of healing dedicated to Asclepius, famed for its acoustically perfect theater.", "region": "Greece"},
    {"id": 15, "name": "Vulci, Italy", "details": "An important Etruscan city that later became part of the Roman Republic, known for its tombs and artworks.", "region": "Italy"},
    {"id": 16, "name": "Cerveteri, Italy", "details": "An ancient Etruscan city famed for its necropolis and burial architecture.", "region": "Italy"},
    {"id": 17, "name": "Stabiae, Italy", "details": "A coastal settlement buried by Vesuvius in 79 CE, known for its luxurious villas.", "region": "Italy"},
    {"id": 18, "name": "Pergamon, Turkey", "details": "A powerful Hellenistic city celebrated for its library, acropolis, and monumental altar.", "region": "Turkey"},
    {"id": 19, "name": "Villa of Cicero, Pompeii", "details": "A villa famed for its frescoes depicting Dionysian initiation rites.", "region": "Italy"},
    {"id": 20, "name": "Unknown", "details": "A location that remains unidentified but is associated with ancient artworks.", "region": "Other"},
    {"id": 21, "name": "Dion, Greece", "details": "A Macedonian sanctuary city at the foot of Mount Olympus, sacred to Zeus and the gods.", "region": "Greece"},
    {"id": 22, "name": "Milos, Greece", "details": "A Cycladic island known for its rich marble resources and famous sculptures.", "region": "Greece"},
    {"id": 23, "name": "Lazio, Italy", "details": "The central Italian region surrounding Rome, rich in Roman villas and sanctuaries.", "region": "Italy"},
    {"id": 24, "name": "Antioch, Turkey", "details": "A major Hellenistic and Roman city, once a cultural crossroads of the eastern Mediterranean.", "region": "Turkey"},
    {"id": 25, "name": "Locri, Italy", "details": "An important city of Magna Graecia in southern Italy, noted for its sanctuaries and art.", "region": "Italy"},
    {"id": 26, "name": "Delos, Greece", "details": "A sacred island in the Cyclades, mythical birthplace of Apollo and Artemis.", "region": "Greece"},
    {"id": 27, "name": "Olympia, Greece", "details": "The sanctuary of Zeus and birthplace of the Olympic Games.", "region": "Greece"},
    {"id": 28, "name": "Ephesus, Turkey", "details": "A wealthy ancient city famed for the Temple of Artemis, one of the Seven Wonders of the Ancient World.", "region": "Turkey"},
    {"id": 29, "name": "Pula, Croatia", "details": "A Roman city on the Adriatic coast, best known for its well-preserved amphitheater.", "region": "Other"},
    {"id": 30, "name": "Villa Adriana", "details": "The vast Roman villa complex of Emperor Hadrian near Tivoli, blending Roman and Greek styles.", "region": "Italy"}
]


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
    query = f"""
    SELECT
    -- grab all needed information
    Artwork.id,
    Artwork.art_name,
    Artwork.type,
    Artwork.years,
    Century.century,
    Century.time_period,
    FoundLocation.found_location,
    CurrentLocation.current_location
    FROM Artwork
    -- joing century, foundlocation, and currentlocation table onto the artwork table
    JOIN Century ON Artwork.century_id = Century.id
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    WHERE Artwork.id IN ({placeholders}) -- only executes query for featured artworks
    ORDER BY Artwork.art_name ASC;
    """
    cur = db.execute(query, featured) # execute query
    art = cur.fetchall()
    return render_template("home.html", title="Home", art=art)


# Page displaying all the artworks
@app.route('/all_artworks')
def all_artworks():
    db = get_db()
    cur = db.execute("""
    SELECT
    -- select all needed information
    Artwork.id,
    Artwork.art_name,
    Artwork.type,
    Artwork.years,
    FoundLocation.found_location,
    CurrentLocation.current_location,
    Century.century,
    Century.time_period
    FROM Artwork
    -- connect artwork table to foundlocation, currentlocation, and currentlocation table
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    JOIN Century ON Artwork.century_id = Century.id
""")
    art = cur.fetchall()
    return render_template("all_art.html", title="All Art", art=art)


# My found location page
@app.route("/location")
def locations_page():
    # Page shows all found locations with blurbs
    return render_template("locations.html", locations=locations)


# Individual artworks for all found locations
@app.route('/locations/<int:id>')
def seperate_locations(id):
    db = get_db()
    cursor = db.execute("""
        SELECT *
        FROM Artwork -- select all from artwork table and foundlocation table
        JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
        -- only fetching the information when it connects to the id
        WHERE FoundLocation.id = ?""", (id,))
    art = cursor.fetchall()
    # Aborting if the id is not connected to a location
    if not art:
        abort(404)
    location_name = art[0]['found_location'] # 
    return render_template('seperate_location.html', title="Seperate Locations", art=art, location_name=location_name)


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
    -- collect all the information I need
    Artwork.id,
    Artwork.art_name,
    Artwork.type,
    Artwork.years,
    Century.century,
    Century.time_period,
    FoundLocation.found_location,
    CurrentLocation.current_location
    FROM Artwork
    -- join onto the other tables I need
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
    return render_template('period.html', title=f"{period_name} Artwork", art=art)


# Page for all the characters
@app.route('/characters')
def characters():
    db = get_db()
    cur = db.execute("""
    SELECT
    -- select the information that I need
    Artwork.id,
    Person.id AS person_id,
    Person.name,
    Person.role,
    -- groups all artworks associated with person into a comma-seperated string
    GROUP_CONCAT(Artwork.art_name, ', ') AS artworks
    FROM Person
    -- join onto the person table
    JOIN ArtworkPerson ON Person.id = ArtworkPerson.pid
    JOIN Artwork ON Artwork.id = ArtworkPerson.aid
    GROUP BY Person.id -- group all rows by each person so there is no duplicate information
    ORDER BY Person.name ASC;
    """)
    # returns a list of rows that corresponds to each person (no duplicates)
    people = cur.fetchall()
    return render_template('character.html', title="People", people=people)


# page for each individual type (e.g. fresco)
@app.route('/artworks/<art_type>')
def artwork_types(art_type):
    db = get_db()
    cur = db.execute("""
    SELECT
    -- select certain information
    Artwork.id,
    Artwork.art_name,
    Artwork.type,
    Artwork.years,
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
    """, (art_type.capitalize(),)) # prevents sql injection
    art = cur.fetchall()
    if not art:
        # aborts to error_404 page if no types are found
        abort(404)
    return render_template('artworks.html', title=art_type.capitalize(), art=art)



# All the seperate individual pages for each artwork
@app.route('/seperate_artworks/<int:id>') # seperates artwork pages by its id
def seperate_artworks(id):
    db = get_db()
    cursor = db.execute("""
    SELECT *
    -- got all the information from all the tables
    FROM Artwork
    JOIN FoundLocation ON Artwork.FL_id = FoundLocation.id
    JOIN CurrentLocation ON Artwork.CL_id = CurrentLocation.id
    JOIN Century ON Artwork.century_id = Century.id
    JOIN ArtworkPerson ON Artwork.id = ArtworkPerson.aid
    JOIN Person ON ArtworkPerson.pid = Person.id
    WHERE Artwork.id = ?""", (id,)) # only fetches artwork with specific id
    # Only fetching one piece of info (the artwork)
    row = cursor.fetchone()
    if row is None:
        # aborts if no artwork is found with the id
        abort(404)
    return render_template('seperate.html', title=row["art_name"], row=row)


# Error 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html"), 404


if __name__ == '__main__':
    # TAKE THIS BIT OUT BEFORE SUMBIT
    app.run(debug=True)
