import sqlite3
from flask import Flask, render_template, request, redirect, flash, url_for, session

app = Flask(__name__, template_folder="templates")
app.secret_key = "demo_secret_key"


# ---------------- Database ----------------

def get_db():
    conn = sqlite3.connect("day_relationships.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS subjects(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS SCORE(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            subject_id INTEGER,
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        )
    """)

    conn.commit()
    conn.close()


# ---------------- Home ----------------

@app.route("/")
def Home():

    conn = get_db()

    students_raw = conn.execute(
        "SELECT * FROM SCORE"
    ).fetchall()

    students_joined = conn.execute("""
        SELECT
            SCORE.id,
            SCORE.name AS student_name,
            subjects.name AS subject_name
        FROM SCORE
        LEFT JOIN subjects
        ON SCORE.subject_id = subjects.id
    """).fetchall()

    conn.close()

    return render_template(
        "Home.html",
        students_raw=students_raw,
        students_joined=students_joined
    )


# ---------------- Subjects ----------------

@app.route("/subjects", methods=["GET", "POST"])
def subjects():

    if request.method == "POST":

        name = request.form["name"].strip()

        conn = get_db()

        conn.execute(
            "INSERT INTO subjects(name) VALUES(?)",
            (name,)
        )

        conn.commit()
        conn.close()

        flash("Subject Added Successfully")

        return redirect(url_for("Home"))

    return render_template("subjects.html")


# ---------------- Register ----------------

@app.route("/Register", methods=["GET", "POST"])
def Register():

    conn = get_db()

    subjects_list = conn.execute(
        "SELECT * FROM subjects"
    ).fetchall()

    if request.method == "POST":

        name = request.form["name"]
        subject_id = request.form["subject_id"]

        conn.execute(
            "INSERT INTO SCORE(name,subject_id) VALUES(?,?)",
            (name, subject_id)
        )

        conn.commit()
        conn.close()

        flash("Student Added Successfully")

        return redirect(url_for("Home"))

    return render_template(
        "Register.html",
        subjects=subjects_list
    )


# ---------------- Dummy Routes (Template Support) ----------------

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/students")
def students():
    return redirect(url_for("Home"))


@app.route("/filter")
def filter():
    return redirect(url_for("Home"))


@app.route("/login")
def login():
    session["username"] = "Admin"
    session["role"] = "admin"
    return redirect(url_for("Home"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("Home"))


@app.route("/explore_technology")
def explore_technology():
    return redirect(url_for("Home"))


@app.route("/explore_programing_lang")
def explore_programing_lang():
    return redirect(url_for("Home"))


@app.route("/explore_computer_science")
def explore_computer_science():
    return redirect(url_for("Home"))


@app.route("/Add_Question")
def Add_Question():
    return redirect(url_for("Home"))


@app.route("/add_student")
def add_student():
    return redirect(url_for("Register"))


# ---------------- Main ----------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5004)