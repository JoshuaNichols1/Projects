from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)


@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def home():
    return render_template("index.html", title="Home")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        return redirect(url_for("index"))
    else:
        return render_template("login.html", title="Login")


@app.route("/profile", methods=["GET"])
def profile(username):
    return render_template("profile.html", title="Profile", username=username)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        connection = sqlite3.connect("C:\sqlite\ taskmanager.db")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO user (username, email, password) VALUES (?, ?, ?)",
            (username, email, password),
        )
        return redirect(url_for("index"))
    return render_template("register.html", title="Register")


if __name__ == "__main__":
    app.run(debug=True)
