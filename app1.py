
import flask
from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import get_db, init_db
from groq import Groq
import os
import sqlite3
import random
import re
import smtplib
from email.message import EmailMessage
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key='linkkiwi2026' #needed for flashing message

def generate_verification_code(length=6):
    return ''.join(random.choices('0123456789', k=length))


def is_valid_email(email):
    return bool(re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email))


def is_email_server_configured():
    return all(os.environ.get(var) for var in ('MAIL_SERVER', 'MAIL_PORT', 'MAIL_USERNAME', 'MAIL_PASSWORD'))


def send_verification_email(to_email, code):
    if not is_email_server_configured():
        return False

    message = EmailMessage()
    message['Subject'] = 'Study Master Pro Email Verification'
    message['From'] = os.environ.get('MAIL_USERNAME')
    message['To'] = to_email
    message.set_content(f"Your verification code is: {code}")

    try:
        smtp_server = os.environ.get('MAIL_SERVER')
        smtp_port = int(os.environ.get('MAIL_PORT'))
        smtp_user = os.environ.get('MAIL_USERNAME')
        smtp_password = os.environ.get('MAIL_PASSWORD')
        use_tls = os.environ.get('MAIL_USE_TLS', 'true').lower() in ('true', '1', 'yes')

        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        if use_tls:
            server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(message)
        server.quit()
        return True
    except Exception as exc:
        print('Email send failed:', exc)
        return False


@app.route('/IMAGES/<path:filename>')
def images(filename):
    return flask.send_from_directory(os.path.join(app.root_path, 'IMAGES'), filename)

QUESTIONS = [
    {

        
        "q": "Q1. What does HTML stand for?",
        "options": [
            "Hyper Text Markup Language",
            "High Text Machine Language",
            "Hyper Transfer Markup Language",
            "Home Tool Markup Language"
        ],
        "answer": "Hyper Text Markup Language"
    },
    {
        "q": "Q2. Which HTML tag is used to create a hyperlink?",
        "options": ["<a>", "<link>", "<href>", "<url>"],
        "answer": "<a>"
    },
    {
        "q": "Q3. Which HTML tag is used to define the title of a webpage?",
        "options": ["<title>", "<head>", "<meta>", "<body>"],
        "answer": "<title>"
    }
]

QUESTIONS1 = [
    {
        "q": "Q1. What does AI stand for?",
        "options": [
            "Artificial Intelligence",
            "Automatic Intelligence",
            "Advanced Internet",
            "Artificial Internet"
        ],
        "answer": "Artificial Intelligence"
    },
    {
        "q": "Q2. Which of the following is a branch of AI?",
        "options": [
            "Machine Learning",
            "Web Hosting",
            "Networking",
            "Cloud Storage"
        ],
        "answer": "Machine Learning"
    },
    {
        "q": "Q3. Which AI approach uses examples and data to improve performance?",
        "options": [
            "Machine Learning",
            "Web Design",
            "Network Security",
            "Database Management"
        ],
        "answer": "Machine Learning"
    }
]

QUESTIONS2 = [
    {
        "q": "Q1. What is Data Science?",
        "options": [
            "Study of data to gain insights",
            "Web Development",
            "Computer Networking",
            "Operating System"
        ],
        "answer": "Study of data to gain insights"
    },
    {
        "q": "Q2. Which language is most popular in Data Science?",
        "options": [
            "Python",
            "HTML",
            "CSS",
            "PHP"
        ],
        "answer": "Python"
    },
    {
        "q": "Q3. Which Python library is commonly used for data visualization?",
        "options": [
            "Matplotlib",
            "Flask",
            "React",
            "Docker"
        ],
        "answer": "Matplotlib"
    }
]

QUESTIONS3 = [
    {
        "q": "Q1. What is Cloud Computing?",
        "options": [
            "Delivering computing services over the Internet",
            "Building websites",
            "Creating databases",
            "Computer repair"
        ],
        "answer": "Delivering computing services over the Internet"
    },
    {
        "q": "Q2. Which of the following is a Cloud Service Provider?",
        "options": [
            "AWS",
            "HTML",
            "CSS",
            "Bootstrap"
        ],
        "answer": "AWS"
    },
    {
        "q": "Q3. What does SaaS stand for?",
        "options": [
            "Software as a Service",
            "System as a Service",
            "Storage as a Service",
            "Security as a Service"
        ],
        "answer": "Software as a Service"
    }
]

QUESTIONS4 = [
    {
        "q": "Q1. What is Cyber Security?",
        "options": [
            "Protecting systems and data from cyber attacks",
            "Creating websites",
            "Building databases",
            "Computer manufacturing"
        ],
        "answer": "Protecting systems and data from cyber attacks"
    },
    {
        "q": "Q2. What is a Virus?",
        "options": [
            "A malicious software",
            "A programming language",
            "A web browser",
            "A database"
        ],
        "answer": "A malicious software"
    },
    {
        "q": "Q3. What does phishing usually try to steal?",
        "options": [
            "Passwords and personal information",
            "Hardware components",
            "Programming code",
            "Network cables"
        ],
        "answer": "Passwords and personal information"
    }
]

QUESTIONS5 = [
    {
        "q": "Q1. What is Mobile App Development?",
        "options": [
            "Creating applications for mobile devices",
            "Building computer hardware",
            "Managing databases",
            "Creating networks"
        ],
        "answer": "Creating applications for mobile devices"
    },
    {
        "q": "Q2. Which operating system is used by Android devices?",
        "options": [
            "Android",
            "iOS",
            "Windows",
            "Linux"
        ],
        "answer": "Android"
    },
    {
        "q": "Q3. Which programming language is commonly used for Android app development?",
        "options": [
            "Kotlin",
            "HTML",
            "SQL",
            "CSS"
        ],
        "answer": "Kotlin"
    }
]

QUESTIONS_C = [
    {
        "q": "Q1. Who is known as the father of C language?",
        "options": [
            "Dennis Ritchie",
            "Bjarne Stroustrup",
            "James Gosling",
            "Guido van Rossum"
        ],
        "answer": "Dennis Ritchie"
    },
    {
        "q": "Q2. In which year was C language developed?",
        "options": [
            "1972",
            "1985",
            "1995",
            "2000"
        ],
        "answer": "1972"
    },
    {
        "q": "Q3. Which symbol ends a statement in C?",
        "options": [
            ";",
            "?",
            "!",
            "/"
        ],
        "answer": ";"
    }
]

QUESTIONS_CPP = [
    {
        "q": "Q1. Who developed C++ language?",
        "options": [
            "Bjarne Stroustrup",
            "Dennis Ritchie",
            "James Gosling",
            "Guido van Rossum"
        ],
        "answer": "Bjarne Stroustrup"
    },
    {
        "q": "Q2. C++ is an extension of which language?",
        "options": [
            "C",
            "Java",
            "Python",
            "Assembly"
        ],
        "answer": "C"
    },
    {
        "q": "Q3. Which feature is supported by C++ but not plain C?",
        "options": [
            "Classes",
            "Pointers",
            "Preprocessor",
            "Functions"
        ],
        "answer": "Classes"
    }
]

QUESTIONS_JAVA = [
    {
        "q": "Q1. Who developed Java programming language?",
        "options": [
            "James Gosling",
            "Dennis Ritchie",
            "Bjarne Stroustrup",
            "Guido van Rossum"
        ],
        "answer": "James Gosling"
    },
    {
        "q": "Q2. Java was developed at which company?",
        "options": [
            "Sun Microsystems",
            "Microsoft",
            "Google",
            "Apple"
        ],
        "answer": "Sun Microsystems"
    },
    {
        "q": "Q3. Java applications typically run on the ______.",
        "options": [
            "Java Virtual Machine",
            "Linux kernel",
            "Web server",
            "Database server"
        ],
        "answer": "Java Virtual Machine"
    }
]

QUESTIONS_PYTHON = [
    {
        "q": "Q1. Who developed Python language?",
        "options": [
            "Guido van Rossum",
            "Dennis Ritchie",
            "James Gosling",
            "Bjarne Stroustrup"
        ],
        "answer": "Guido van Rossum"
    },
    {
        "q": "Q2. Python is which type of language?",
        "options": [
            "Interpreted language",
            "Compiled language",
            "Machine language",
            "Assembly language"
        ],
        "answer": "Interpreted language"
    },
    {
        "q": "Q3. Which symbol begins a comment in Python?",
        "options": [
            "#",
            "//",
            "/*",
            "--"
        ],
        "answer": "#"
    }

]

QUESTIONS_OS = [
    {
        "q": "Q1. What is an Operating System?",
        "options": [
            "System software that manages hardware and software",
            "A programming language",
            "A web browser",
            "A database system"
        ],
        "answer": "System software that manages hardware and software"
    },
    {
        "q": "Q2. Which of the following is an Operating System?",
        "options": [
            "Windows",
            "Java",
            "HTML",
            "MySQL"
        ],
        "answer": "Windows"
    },
    {
        "q": "Q3. Which OS component controls hardware and manages resources?",
        "options": [
            "Operating System",
            "Web Server",
            "Database",
            "Programming Language"
        ],
        "answer": "Operating System"
    }
]

QUESTIONS_DBMS = [
    {
        "q": "Q1. What is DBMS?",
        "options": [
            "Software to manage and store data",
            "Programming language",
            "Operating system",
            "Web browser"
        ],
        "answer": "Software to manage and store data"
    },
    {
        "q": "Q2. Which of the following is a DBMS?",
        "options": [
            "MySQL",
            "Java",
            "Linux",
            "HTML"
        ],
        "answer": "MySQL"
    },
    {
        "q": "Q3. Which SQL command is used to retrieve data from a database?",
        "options": [
            "SELECT",
            "SAVE",
            "DELETE",
            "OPEN"
        ],
        "answer": "SELECT"
    }
]

QUESTIONS_CN = [
    {
        "q": "Q1. What is a computer network?",
        "options": [
            "A system of connected computers to share data",
            "A type of software",
            "A programming language",
            "A database system"
        ],
        "answer": "A system of connected computers to share data"
    },
    {
        "q": "Q2. What does LAN stand for?",
        "options": [
            "Local Area Network",
            "Large Area Network",
            "Light Access Network",
            "Logical Area Network"
        ],
        "answer": "Local Area Network"
    },
    {
        "q": "Q3. Which device is used to route traffic between networks?",
        "options": [
            "Router",
            "Scanner",
            "Printer",
            "Monitor"
        ],
        "answer": "Router"
    }
]

QUESTIONS_DS = [
    {
        "q": "Q1. What is a data structure?",
        "options": [
            "A way to organize and store data",
            "A programming language",
            "An operating system",
            "A database software"
        ],
        "answer": "A way to organize and store data"
    },
    {
        "q": "Q2. Which data structure follows LIFO principle?",
        "options": [
            "Stack",
            "Queue",
            "Array",
            "Tree"
        ],
        "answer": "Stack"
    },
    {
        "q": "Q3. Which data structure follows FIFO principle?",
        "options": [
            "Queue",
            "Stack",
            "Tree",
            "Graph"
        ],
        "answer": "Queue"
    }
]

stud = [
    {
        'Sr_no':1,
        'Name':'John Doe',
        'username':'John',
        'email':'John@gmail.com',
        'password':'John@1234'
    },
    {
        'Sr_no':2,
        'Name':'Jane smith',
        'username':'Jone',
        'email':'Jane@gmail.com',
        'password':'Jone@1234'
    }
]

@app.route('/')
def Home():
    return flask.render_template('home.html',students=stud)
    
    
    



@app.route('/login', methods=['GET', 'POST'])
def login():

    if flask.request.method == 'POST':

        username = flask.request.form.get('username')
        password = flask.request.form.get('password')

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM SCORE WHERE Username = ?",
            (username,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user['Password'], password):

            if user['email_verified'] != 1:
                verification_code = generate_verification_code()
                flask.session['pending_verification'] = user['Username']
                flask.session['verification_code'] = verification_code
                flask.session['verification_email'] = user['Email']

                if send_verification_email(user['Email'], verification_code):
                    flask.flash('Your email is not verified. A verification code was sent to your email.', 'warning')
                else:
                    flask.flash('Your email is not verified. Email sending is not configured; use the code shown on the verification page.', 'warning')

                return flask.redirect(flask.url_for('verify_email'))

            flask.session['username'] = user['Username']
            flask.session['student_name'] = user['Student_name']
            flask.session['role'] = user['role']
            flask.flash('Login Successful!', 'success')
            return flask.redirect(flask.url_for('technology'))

        else:
            flask.flash('Invalid Username or Password!', 'danger')

    return flask.render_template('login.html')


@app.route('/verify_email', methods=['GET', 'POST'])
def verify_email():
    username = flask.session.get('pending_verification')
    verification_code = flask.session.get('verification_code')
    email = flask.session.get('verification_email')

    if not username or not verification_code or not email:
        flask.flash('No email verification is in progress.', 'danger')
        return flask.redirect(flask.url_for('Register'))

    if flask.request.method == 'POST':
        entered_code = flask.request.form.get('code', '').strip()

        if entered_code == verification_code:
            conn = get_db()
            conn.execute(
                "UPDATE SCORE SET email_verified = 1 WHERE Username = ?",
                (username,)
            )
            conn.commit()
            conn.close()

            flask.session.pop('pending_verification', None)
            flask.session.pop('verification_code', None)
            flask.session.pop('verification_email', None)

            flask.flash('Email verified successfully! You can now login.', 'success')
            return flask.redirect(flask.url_for('login'))

        flask.flash('Invalid verification code. Please try again.', 'danger')

    return flask.render_template(
        'verify_email.html',
        email=email,
        show_code=not is_email_server_configured(),
        code=verification_code if not is_email_server_configured() else None
    )


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():

    if flask.request.method == 'POST':

        username = flask.request.form.get('username')
        email = flask.request.form.get('email')
        new_password = flask.request.form.get('new_password')

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM SCORE WHERE Username=? AND Email=?",
            (username, email)
        ).fetchone()

        if user:

            hashed_password = generate_password_hash(new_password)

            conn.execute(
                "UPDATE SCORE SET Password=? WHERE Username=?",
                (hashed_password, username)
            )

            conn.commit()

            flask.flash('Password Updated Successfully!', 'success')

            conn.close()

            return flask.redirect(flask.url_for('Login'))

        else:

            conn.close()

            flask.flash('Invalid Username or Email!', 'danger')

            return flask.redirect(flask.url_for('forgot_password'))

    return flask.render_template('forgot_password.html')

@app.route('/explore_technology')
def explore_technology():

    if 'sr_no' in flask.session:
        return flask.redirect(flask.url_for('technology'))

    flask.flash('Please Login or Register First!')
    return flask.redirect(flask.url_for('login'))


@app.route('/technology')
def technology():
    return flask.render_template('technology.html')

@app.route('/web_development/<int:qno>', methods=['GET', 'POST'])
def web_development(qno):

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("Web Development",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Web Development Questions Found!</h2>"

    if "score" not in flask.session:
        flask.session["score"] = 0

    if flask.request.method == "POST":

        selected = flask.request.form.get("answer")
        flask.session[f"q{qno}"] = selected

        if "next" in flask.request.form and qno < len(all_questions) - 1:
            return flask.redirect(flask.url_for("web_development", qno=qno + 1))

        if "prev" in flask.request.form and qno > 0:
            return flask.redirect(flask.url_for("web_development", qno=qno - 1))

        if "submit" in flask.request.form:

            score = 0

            for i in range(len(all_questions)):
                if flask.session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            flask.session["score"] = score

            return flask.redirect(flask.url_for("Result"))

    return flask.render_template(
        "web_development.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions)
    )


@app.route('/Artificial_Intelligence/<int:qno>', methods=['GET', 'POST'])
def Artificial_Intelligence(qno):

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("Artificial Intelligence",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS1.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Artificial Intelligence Questions Found!</h2>"

    if "score" not in flask.session:
        flask.session["score"] = 0

    if flask.request.method == "POST":

        selected = flask.request.form.get("answer")
        flask.session[f"q{qno}"] = selected

        if "next" in flask.request.form and qno < len(all_questions) - 1:
            return flask.redirect(flask.url_for("Artificial_Intelligence", qno=qno + 1))

        if "prev" in flask.request.form and qno > 0:
            return flask.redirect(flask.url_for("Artificial_Intelligence", qno=qno - 1))

        if "submit" in flask.request.form:

            score = 0

            for i in range(len(all_questions)):
                if flask.session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            flask.session["score"] = score

            return flask.redirect(flask.url_for("Result"))

    return flask.render_template(
        "Artificial_Intelligence.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions)
    )

@app.route('/data_science/<int:qno>', methods=['GET', 'POST'])
def data_science(qno):

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("Data Science",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS2.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Data Science Questions Found!</h2>"

    if "score" not in flask.session:
        flask.session["score"] = 0

    if flask.request.method == "POST":

        selected = flask.request.form.get("answer")
        flask.session[f"q{qno}"] = selected

        if "next" in flask.request.form and qno < len(all_questions) - 1:
            return flask.redirect(flask.url_for("data_science", qno=qno + 1))

        if "prev" in flask.request.form and qno > 0:
            return flask.redirect(flask.url_for("data_science", qno=qno - 1))

        if "submit" in flask.request.form:

            score = 0

            for i in range(len(all_questions)):
                if flask.session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            flask.session["score"] = score

            return flask.redirect(flask.url_for("Result"))

    return flask.render_template(
        "data_science.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions)
    )

@app.route('/cloud_computing/<int:qno>', methods=['GET', 'POST'])
def cloud_computing(qno):

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("Cloud Computing",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS3.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Cloud Computing Questions Found!</h2>"

    if "score" not in flask.session:
        flask.session["score"] = 0

    if flask.request.method == "POST":

        selected = flask.request.form.get("answer")
        flask.session[f"q{qno}"] = selected

        if "next" in flask.request.form and qno < len(all_questions) - 1:
            return flask.redirect(flask.url_for("cloud_computing", qno=qno + 1))

        if "prev" in flask.request.form and qno > 0:
            return flask.redirect(flask.url_for("cloud_computing", qno=qno - 1))

        if "submit" in flask.request.form:

            score = 0

            for i in range(len(all_questions)):
                if flask.session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            flask.session["score"] = score

            return flask.redirect(flask.url_for("Result"))

    return flask.render_template(
        "cloud_computing.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions)
    )

@app.route('/cyber_security/<int:qno>', methods=['GET', 'POST'])
def cyber_security(qno):

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("Cyber Security",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS4.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Cyber Security Questions Found!</h2>"

    if "score" not in flask.session:
        flask.session["score"] = 0

    if flask.request.method == "POST":

        selected = flask.request.form.get("answer")
        flask.session[f"q{qno}"] = selected

        if "next" in flask.request.form and qno < len(all_questions) - 1:
            return flask.redirect(flask.url_for("cyber_security", qno=qno + 1))

        if "prev" in flask.request.form and qno > 0:
            return flask.redirect(flask.url_for("cyber_security", qno=qno - 1))

        if "submit" in flask.request.form:

            score = 0

            for i in range(len(all_questions)):
                if flask.session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            flask.session["score"] = score

            return flask.redirect(flask.url_for("Result"))

    return flask.render_template(
        "cyber_security.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions)
    )

@app.route('/mobile_app_development/<int:qno>', methods=['GET', 'POST'])
def Mobile_App_Development(qno):

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("Mobile_App_Development",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS5.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Mobile App Development Questions Found!</h2>"

    if "score" not in flask.session:
        flask.session["score"] = 0

    if flask.request.method == "POST":

        selected = flask.request.form.get("answer")

        flask.session[f"q{qno}"] = selected

        # NEXT
        if "next" in flask.request.form and qno < len(all_questions) - 1:
            return flask.redirect(flask.url_for("Mobile_App_Development", qno=qno + 1))

        # PREVIOUS
        if "prev" in flask.request.form and qno > 0:
            return flask.redirect(flask.url_for("Mobile_App_Development", qno=qno - 1))

        # SUBMIT
        if "submit" in flask.request.form:

            score = 0

            for i in range(len(all_questions)):
                if flask.session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            flask.session["score"] = score

            return flask.redirect(flask.url_for("Result"))

    return flask.render_template(
        "mobile_app_development.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions)
    )




@app.route('/explore_programing_lang')
def explore_programing_lang():

    if 'sr_no' in flask.session:
        return flask.redirect(flask.url_for('programing_lang'))

    flask.flash('Please Login or Register First!')
    return flask.redirect(flask.url_for('login'))

@app.route('/programing_lang')
def programing_lang():
    return flask.render_template('programing_lang.html')


@app.route('/c_lang/<int:qno>', methods=['GET', 'POST'])
def c_lang(qno):

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("C",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS_C.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No C Questions Found!</h2>"

    if "score" not in flask.session:
        flask.session["score"] = 0

    if flask.request.method == "POST":

        selected = flask.request.form.get("answer")
        flask.session[f"q{qno}"] = selected

        if "next" in flask.request.form and qno < len(all_questions) - 1:
            return flask.redirect(flask.url_for("c_lang", qno=qno + 1))

        if "prev" in flask.request.form and qno > 0:
            return flask.redirect(flask.url_for("c_lang", qno=qno - 1))

        if "submit" in flask.request.form:

            score = 0

            for i in range(len(all_questions)):
                if flask.session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            flask.session["score"] = score

            return flask.redirect(flask.url_for("Result"))

    return flask.render_template(
        "c_lang.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions)
    )


@app.route('/cpp_lang/<int:qno>', methods=['GET', 'POST'])
def cpp_lang(qno):

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("C++",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS_CPP.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No C++ Questions Found!</h2>"

    if "score" not in flask.session:
        flask.session["score"] = 0

    if flask.request.method == "POST":

        selected = flask.request.form.get("answer")
        flask.session[f"q{qno}"] = selected

        if "next" in flask.request.form and qno < len(all_questions) - 1:
            return flask.redirect(flask.url_for("cpp_lang", qno=qno + 1))

        if "prev" in flask.request.form and qno > 0:
            return flask.redirect(flask.url_for("cpp_lang", qno=qno - 1))

        if "submit" in flask.request.form:

            score = 0

            for i in range(len(all_questions)):
                if flask.session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            flask.session["score"] = score

            return flask.redirect(flask.url_for("Result"))

    return flask.render_template(
        "cpp_lang.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions)
    )

@app.route('/java_lang/<int:qno>', methods=['GET', 'POST'])
def java_lang(qno):

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("Java",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS_JAVA.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Java Questions Found!</h2>"

    if "score" not in flask.session:
        flask.session["score"] = 0

    if flask.request.method == "POST":

        selected = flask.request.form.get("answer")
        flask.session[f"q{qno}"] = selected

        if "next" in flask.request.form and qno < len(all_questions) - 1:
            return flask.redirect(flask.url_for("java_lang", qno=qno + 1))

        if "prev" in flask.request.form and qno > 0:
            return flask.redirect(flask.url_for("java_lang", qno=qno - 1))

        if "submit" in flask.request.form:

            score = 0

            for i in range(len(all_questions)):
                if flask.session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            flask.session["score"] = score

            return flask.redirect(flask.url_for("Result"))

    return flask.render_template(
        "java_lang.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions)
    )

@app.route('/python_lang/<int:qno>', methods=['GET', 'POST'])
def python_lang(qno):

    # Database madhun Python questions ghya
    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("Python",)
    ).fetchall()

    conn.close()

    # Pahile dictionary madhle questions
    all_questions = QUESTIONS_PYTHON.copy()

    # Database madhle questions add kara
    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    # Questions nasel tar
    if len(all_questions) == 0:
        return "<h2>No Python Questions Found!</h2>"

    if "score" not in flask.session:
        flask.session["score"] = 0

    # POST Request
    if flask.request.method == "POST":

        selected = flask.request.form.get("answer")

        # User answer save kara
        flask.session[f"q{qno}"] = selected

        # Next button
        if "next" in flask.request.form and qno < len(all_questions) - 1:
            return flask.redirect(flask.url_for("python_lang", qno=qno + 1))

        # Previous button
        if "prev" in flask.request.form and qno > 0:
            return flask.redirect(flask.url_for("python_lang", qno=qno - 1))

        # Submit button
        if "submit" in flask.request.form:

            score = 0

            for i in range(len(all_questions)):
                if flask.session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            flask.session["score"] = score

            return flask.redirect(flask.url_for("Result"))

    return flask.render_template(
        "python_lang.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions)
    )


@app.route('/explore_computer_science')
def explore_computer_science():

    if 'sr_no' in flask.session:
        return flask.redirect(flask.url_for('computer_science'))

    flask.flash('Please Login or Register First!')
    return flask.redirect(flask.url_for('login'))

@app.route('/computer_science')
def computer_science():
    return flask.render_template('Computer_seience.html')


@app.route('/operating_system/<int:qno>', methods=['GET', 'POST'])
def operating_system(qno):

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("Operating System",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS_OS.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Operating System Questions Found!</h2>"

    if "score" not in flask.session:
        flask.session["score"] = 0

    if flask.request.method == "POST":

        selected = flask.request.form.get("answer")
        flask.session[f"q{qno}"] = selected

        if "next" in flask.request.form and qno < len(all_questions) - 1:
            return flask.redirect(flask.url_for("operating_system", qno=qno + 1))

        if "prev" in flask.request.form and qno > 0:
            return flask.redirect(flask.url_for("operating_system", qno=qno - 1))

        if "submit" in flask.request.form:

            score = 0

            for i in range(len(all_questions)):
                if flask.session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            flask.session["score"] = score

            return flask.redirect(flask.url_for("Result"))

    return flask.render_template(
        "operating_system.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions)
    )


@app.route('/dbms_lang/<int:qno>', methods=['GET', 'POST'])
def dbms_lang(qno):

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("DBMS",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS_DBMS.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No DBMS Questions Found!</h2>"

    if "score" not in flask.session:
        flask.session["score"] = 0

    if flask.request.method == "POST":

        selected = flask.request.form.get("answer")
        flask.session[f"q{qno}"] = selected

        if "next" in flask.request.form and qno < len(all_questions) - 1:
            return flask.redirect(flask.url_for("dbms_lang", qno=qno + 1))

        if "prev" in flask.request.form and qno > 0:
            return flask.redirect(flask.url_for("dbms_lang", qno=qno - 1))

        if "submit" in flask.request.form:

            score = 0

            for i in range(len(all_questions)):
                if flask.session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            flask.session["score"] = score

            return flask.redirect(flask.url_for("Result"))

    return flask.render_template(
        "dbms_lang.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions)
    )

@app.route('/computer_network/<int:qno>', methods=['GET', 'POST'])
def computer_network(qno):

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("Computer Network",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS_CN.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Computer Network Questions Found!</h2>"

    if "score" not in flask.session:
        flask.session["score"] = 0

    if flask.request.method == "POST":

        selected = flask.request.form.get("answer")
        flask.session[f"q{qno}"] = selected

        if "next" in flask.request.form and qno < len(all_questions) - 1:
            return flask.redirect(flask.url_for("computer_network", qno=qno + 1))

        if "prev" in flask.request.form and qno > 0:
            return flask.redirect(flask.url_for("computer_network", qno=qno - 1))

        if "submit" in flask.request.form:

            score = 0

            for i in range(len(all_questions)):
                if flask.session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            flask.session["score"] = score

            return flask.redirect(flask.url_for("Result"))

    return flask.render_template(
        "computer_network.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions)
    )

@app.route('/data_structure/<int:qno>', methods=['GET', 'POST'])
def data_structure(qno):

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM QUESTIONS WHERE subject=?",
        ("Data Structure",)
    ).fetchall()

    conn.close()

    all_questions = QUESTIONS_DS.copy()

    for row in rows:
        all_questions.append({
            "q": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"]
        })

    if len(all_questions) == 0:
        return "<h2>No Data Structure Questions Found!</h2>"

    if "score" not in flask.session:
        flask.session["score"] = 0

    if flask.request.method == "POST":

        selected = flask.request.form.get("answer")
        flask.session[f"q{qno}"] = selected

        if "next" in flask.request.form and qno < len(all_questions) - 1:
            return flask.redirect(flask.url_for("data_structure", qno=qno + 1))

        if "prev" in flask.request.form and qno > 0:
            return flask.redirect(flask.url_for("data_structure", qno=qno - 1))

        if "submit" in flask.request.form:

            score = 0

            for i in range(len(all_questions)):
                if flask.session.get(f"q{i}") == all_questions[i]["answer"]:
                    score += 1

            flask.session["score"] = score

            return flask.redirect(flask.url_for("Result"))

    return flask.render_template(
        "data_structure.html",
        question=all_questions[qno],
        qno=qno,
        total=len(all_questions)
    )


@app.route('/logout')
def logout():
    
    flask.session.pop('username', None)
    flask.session.pop('role', None)
    flask.flash('You have been logged out.', 'info')
    return flask.redirect(flask.url_for('Home'))

@app.route('/subjects')
def subjects():
    conn=get_db()
    rows = conn.execute('''
                        SELECT subject AS subject_name, COUNT(*) AS student_count
                        FROM SCORE
                        GROUP BY subject
                        ORDER BY subject
                        ''').fetchall()
    conn.close()
    return flask.render_template('subjects.html',rows=rows)



@app.route('/Register', methods=['GET', 'POST'])
def Register():
    #if session.get('role')!='admin':
    #    flash("Admin only! you do not have permission","danger")
    #    return redirect(url_for('Home'))
    
    if flask.request.method == 'POST':

        student_name = flask.request.form.get('student_name')
        username = flask.request.form.get('username')
        email = flask.request.form.get('email')
        password = flask.request.form.get('password')
        subject = flask.request.form.get('subject')

        if not student_name or not username or not email or not password or not subject:
            flask.flash('Please provide all details!', 'danger')
            return flask.redirect(flask.url_for('Register'))

        if not is_valid_email(email):
            flask.flash('Please enter a valid email address.', 'danger')
            return flask.redirect(flask.url_for('Register'))

        conn = get_db()
        existing_user = conn.execute(
            "SELECT * FROM SCORE WHERE Username = ? OR Email = ?",
            (username, email)
        ).fetchone()

        if existing_user:
            conn.close()
            flask.flash('Username or email already exists.', 'danger')
            return flask.redirect(flask.url_for('Register'))

        verification_code = generate_verification_code()

        hashed_password = generate_password_hash(password)

        conn.execute(
            '''
            INSERT INTO SCORE
            (Student_name, total_marks, Username, Email, Password, Subject, email_verified)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (student_name, 0, username, email, hashed_password, subject, 0)
        )

        conn.commit()
        conn.close()

        flask.session['pending_verification'] = username
        flask.session['verification_code'] = verification_code
        flask.session['verification_email'] = email

        if send_verification_email(email, verification_code):
            flask.flash('Registration successful! A verification code has been sent to your email.', 'success')
        else:
            flask.flash('Registration successful! Email sending is not configured, so your verification code is shown on the next page.', 'warning')

        return flask.redirect(flask.url_for('verify_email'))

    return flask.render_template('Register.html')


@app.route('/search')
def search():
    q = flask.request.args.get('q', '')
    conn = get_db()

    if q:
        students = conn.execute(
            '''SELECT * FROM SCORE
               WHERE Student_name LIKE ?
               OR Username LIKE ?''',
            (f'%{q}%', f'%{q}%')
        ).fetchall()
    else:
        students = conn.execute(
            'SELECT * FROM SCORE ORDER BY Sr_no ASC'
        ).fetchall()

    conn.close()

    return flask.render_template(
        'search.html',
        students=students,
        query=q
    )



@app.route('/about')
def about():
    return flask.render_template('about.html')

@app.route('/sum', methods=['GET', 'POST'])
def sum_page():
    num1 = ''
    num2 = ''
    result = None
    error = None

    if flask.request.method == 'POST':
        num1 = flask.request.form.get('num1', '').strip()
        num2 = flask.request.form.get('num2', '').strip()

        try:
            result = float(num1) + float(num2)
        except ValueError:
            error = 'Please enter two valid numbers.'

    return flask.render_template('sum.html', num1=num1, num2=num2, result=result, error=error)

@app.route('/Add_Question', methods=['GET', 'POST'])
def Add_Question():
    
    if flask.request.method == "POST":

        subject = flask.request.form.get('subject')
        question = flask.request.form.get('question')
        option1 = flask.request.form.get('option1')
        option2 = flask.request.form.get('option2')
        option3 = flask.request.form.get('option3')
        option4 = flask.request.form.get('option4')
        answer = flask.request.form.get('answer')

        if not subject or not question or not option1 or not option2 or not option3 or not option4 or not answer:
            flask.flash('Please fill all fields!', 'danger')
            return flask.render_template("Add_Question.html")

        conn = get_db()

        conn.execute(
            '''
            INSERT INTO QUESTIONS
            (subject,question, option1, option2, option3, option4, answer)
            VALUES (?,?, ?, ?, ?, ?, ?)
            ''',
            (subject,question, option1, option2, option3, option4, answer)
        )

        conn.commit()
        conn.close()

        flask.flash("Question Added Successfully!", "success")

        return flask.redirect(flask.url_for('Add_Question'))

    return flask.render_template('Add_Question.html')


@app.route("/students")
def students():
    if flask.session.get('role')!='admin':
        flask.flash("Admin only! you do not have permission","danger")
        return flask.redirect(flask.url_for('Home'))

    conn = get_db()
    db_students = conn.execute(
        'SELECT * FROM SCORE ORDER BY Sr_no ASC'
    ).fetchall()
    conn.close()

    combined_students = []

    # Database Data
    for s in db_students:
        combined_students.append({
        'Sr_no': s['Sr_no'],
        'Name': s['Student_name'],
        'username': s['Username'],
        'email': s['Email']
        #'password': s['Password']
    })

    return flask.render_template(
        "students.html",
        students=combined_students
    )

@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    conn= get_db()
    subjects = conn.execute('SELECT * FROM subjects').fetchall()
    # subjects list - needed to populate the dropdown in the form
    if flask.request.method == "POST":
        name = flask.request.form['name'].strip()
        subject_id = flask.request.form['subject_id']
        conn.execute('INSERT INTO students (name, subject_id) VALUES (?, ?)', (name, subject_id))
        conn.commit()
        conn.close()
        flask.flash(f"Student '{name}' added successfully!")
        return flask.redirect(flask.url_for('students'))
    return flask.render_template("add_student.html", subjects=subjects)
    
@app.route('/view_student/<int:Sr_no>')
def view_student(Sr_no):

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM SCORE WHERE Sr_no=?",
        (Sr_no,)
    ).fetchone()

    conn.close()

    return flask.render_template('view_student.html', students=student)


@app.route('/delete_candidate/<int:Sr_no>')
def delete_candidate(Sr_no):
        

    if flask.session.get('role')!='admin':
        flask.flash("Admin only! you do not have permission","danger")
        return flask.redirect(flask.url_for('Home'))

    conn = get_db()

    student = conn.execute(
            'SELECT * FROM SCORE WHERE Sr_no=?',
            (Sr_no,)
            ).fetchone()
    if student is None:
                flask.flash("student not found","danger")
                conn.close()
            
    conn.execute(
            'DELETE FROM SCORE WHERE Sr_no=?',
            (Sr_no,)
            )
    conn.commit()
    conn.close()
    flask.flash("candidate deleted successfully","success")
    return flask.redirect(flask.url_for('students'))

@app.route('/edit_student/<int:Sr_no>', methods=['GET', 'POST'])
def edit_student(Sr_no):
    if flask.session.get('role')!='admin':
        flask.flash("Admin only! you do not have permission","danger")
        return flask.redirect(flask.url_for('Home'))

    conn = get_db()

    if flask.request.method == 'POST':

        Candidate_name = flask.request.form['Candidate_name']

        conn.execute(
            "UPDATE SCORE SET student_name=? WHERE Sr_no=?",
            (Candidate_name, Sr_no)
        )

        conn.commit()
        conn.close()

        return flask.redirect(flask.url_for('students'))

    student = conn.execute(
        "SELECT * FROM SCORE WHERE Sr_no=?",
        (Sr_no,)
    ).fetchone()

    conn.close()

    return flask.render_template('edit_student.html', student=student)


@app.route('/filter')
def filter():

    subject = flask.request.args.get('subject')

    conn = get_db()

    if subject:
        students = conn.execute(
            "SELECT * FROM SCORE WHERE subject=?",
            (subject,)
        ).fetchall()
    else:
        students = conn.execute(
            "SELECT * FROM SCORE"
        ).fetchall()

    conn.close()

    return flask.render_template(
        'filter_result.html',
        students=students
    )

@app.route('/Subject')
def Subject():
    return flask.render_template('Subject.html')


@app.route('/Result')
def Result():
    score = flask.session.get("score", 0)
    total = len(QUESTIONS)

    return flask.render_template("result.html", score=score, total=total)

@app.route("/pdf_summary")
def pdf_summary():
    return render_template("pdf_summary.html")
@app.route("/ai_quiz")
def ai_quiz_generator():
    return render_template("ai_quiz.html")

init_db()
if __name__ == '__main__':
    
    app.run(debug=True)