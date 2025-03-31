from flask import Flask, render_template


app = Flask(__name__)


@app.route("/home")
def home():
    return render_template("home.html", title="Home")


if __name__ == '__main__':
    # TAKE THIS BIT OUT BEFORE SUMBIT
    app.run(debug=True)
