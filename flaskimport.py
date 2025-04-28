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
    cur.execute("SELECT * FROM Artwork")
    art = cur.fetchall()
    conn.close()
    return render_template("all_art.html", art=art)


if __name__ == '__main__':
    # TAKE THIS BIT OUT BEFORE SUMBIT
    app.run(debug=True)
