import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "sqlite_secret_key"

DATABASE = os.getenv("DATABASE_PATH", "/data/citizens.db")

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    try:
        citizens = conn.execute("SELECT * FROM Citizens").fetchall()
    except sqlite3.OperationalError:
        # Table might not exist yet
        citizens = []
    conn.close()
    return render_template("index.html", citizens=citizens)

@app.route("/add", methods=("GET", "POST"))
def add():
    if request.method == "POST":
        name = request.form["name"]
        species = request.form["species"]
        career = request.form["career"]
        age = request.form["age"]

        if not name:
            flash("Name is required!")
        else:
            conn = get_db_connection()
            try:
                # Using parameter binding for standard CRUD
                conn.execute(
                    "INSERT INTO Citizens (name, species, career, age) VALUES (?, ?, ?, ?)",
                    (name, species, career, age),
                )
                conn.commit()
                conn.close()
                return redirect(url_for("index"))
            except sqlite3.Error as e:
                flash(f"Error: {e}")
                conn.close()

    return render_template("add.html")

@app.route("/edit/<int:id>", methods=("GET", "POST"))
def edit(id):
    conn = get_db_connection()
    citizen = conn.execute("SELECT * FROM Citizens WHERE id = ?", (id,)).fetchone()

    if request.method == "POST":
        name = request.form["name"]
        species = request.form["species"]
        career = request.form["career"]
        age = request.form["age"]

        if not name:
            flash("Name is required!")
        else:
            try:
                conn.execute(
                    "UPDATE Citizens SET name = ?, species = ?, career = ?, age = ? WHERE id = ?",
                    (name, species, career, age, id),
                )
                conn.commit()
                conn.close()
                return redirect(url_for("index"))
            except sqlite3.Error as e:
                flash(f"Error: {e}")

    conn.close()
    return render_template("edit.html", citizen=citizen)

@app.route("/delete/<int:id>", methods=("POST",))
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM Citizens WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Citizen deleted successfully!")
    return redirect(url_for("index"))

@app.route("/security-lab", methods=("GET", "POST"))
def security_lab():
    results = []
    query_display = ""
    mode = "SECURED"
    search_term = ""
    abs_db_path = os.path.abspath(DATABASE)

    if request.method == "POST":
        search_term = request.form["search_term"]
        mode = request.form["mode"]

        conn = get_db_connection()
        if mode == "VULNERABLE":
            # Direct string concatenation - DANGEROUS!
            query_display = f"SELECT * FROM Citizens WHERE name = '{search_term}'"
            try:
                results = conn.execute(query_display).fetchall()
            except sqlite3.Error as e:
                flash(f"SQL Error: {e}")
        else:
            # Parameter Binding - SECURE!
            query_display = "SELECT * FROM Citizens WHERE name = ?"
            try:
                results = conn.execute(query_display, (search_term,)).fetchall()
            except sqlite3.Error as e:
                flash(f"SQL Error: {e}")
        conn.close()

    return render_template("security_lab.html", results=results, query=query_display, mode=mode, search_term=search_term, abs_db_path=abs_db_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
