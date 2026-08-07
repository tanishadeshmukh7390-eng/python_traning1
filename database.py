import os
import sqlite3
import json
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session, send_from_directory
from dotenv import load_dotenv
from ai_quiz_generator import AIQuizGenerator
from pdf_summarizer import PDFSummarizer

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'linkkiwi2026'  # needed for flash messages

# Use a project-local absolute path so the DB is created and accessed
# consistently both locally and on deployments (e.g. PythonAnywhere).
DB_PATH = os.path.join(os.path.dirname(__file__), 'myproject.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS SCORE (
            Sr_no INTEGER PRIMARY KEY AUTOINCREMENT,
            Student_name TEXT NOT NULL,
            Username TEXT NOT NULL,
            Email TEXT NOT NULL,
            Password TEXT NOT NULL,
            subject TEXT NOT NULL,
            email_verified INTEGER DEFAULT 1
        )
    ''')

    try:
        conn.execute("ALTER TABLE SCORE add column total_marks INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    try:
        conn.execute("ALTER TABLE SCORE add column email_verified INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        pass

    try:
        conn.execute("ALTER TABLE SCORE add column role text default 'student'")
    except sqlite3.OperationalError:
        pass



    conn.execute("""
    CREATE TABLE IF NOT EXISTS QUESTIONS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,         
        question TEXT NOT NULL,
        option1 TEXT NOT NULL,
        option2 TEXT NOT NULL,
        option3 TEXT NOT NULL,
        option4 TEXT NOT NULL,
        answer TEXT NOT NULL
    )
    """)

    conn.execute("""
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
)
""")

    conn.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    subject_id INTEGER,
    FOREIGN KEY(subject_id) REFERENCES subjects(id)
)
""")
    
    # Table for AI-generated quizzes
    conn.execute("""
    CREATE TABLE IF NOT EXISTS ai_generated_quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        difficulty TEXT DEFAULT 'intermediate',
        num_questions INTEGER DEFAULT 5,
        quiz_data TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_by TEXT
    )
    """)
    
    # Table for AI quiz attempts/scores
    conn.execute("""
    CREATE TABLE IF NOT EXISTS ai_quiz_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER NOT NULL,
        student_name TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        total_questions INTEGER,
        user_answers TEXT,
        attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(quiz_id) REFERENCES ai_generated_quizzes(id)
    )
    """)
    
    # Table for PDF summaries
    conn.execute("""
    CREATE TABLE IF NOT EXISTS pdf_summaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        original_filename TEXT,
        num_pages INTEGER DEFAULT 0,
        num_questions INTEGER DEFAULT 0,
        summary_text TEXT,
        key_points TEXT,
        topics TEXT,
        difficulty_level TEXT,
        upload_path TEXT,
        uploaded_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Table for PDF-generated questions
    conn.execute("""
    CREATE TABLE IF NOT EXISTS pdf_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        summary_id INTEGER NOT NULL,
        question TEXT NOT NULL,
        options TEXT,
        correct_answer TEXT,
        explanation TEXT,
        difficulty TEXT,
        question_index INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(summary_id) REFERENCES pdf_summaries(id)
    )
    """)
    
    # Table for PDF question attempts
    conn.execute("""
    CREATE TABLE IF NOT EXISTS pdf_question_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER NOT NULL,
        student_name TEXT NOT NULL,
        user_answer TEXT,
        is_correct INTEGER DEFAULT 0,
        attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(question_id) REFERENCES pdf_questions(id)
    )
    """)
    
    default_subjects = ['java','cpp','python','Operating System','Data Science','Database Management']
    
    for subject in default_subjects:
        try:
            conn.execute("INSERT INTO subjects (name) VALUES (?)", (subject,))
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

init_db()  # function call

# ==================== BASIC APP ROUTES ====================

@app.route('/')
def Home():
    """Home page"""
    return render_template('home.html')

@app.route('/home')
def home():
    """Home page alias"""
    return redirect(url_for('Home'))

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/sum')
def sum_page():
    """Sum page"""
    return render_template('sum.html')

@app.route('/students')
def students():
    """Students list page"""
    return render_template('student.html')

@app.route('/subjects')
def subjects():
    """Subjects page"""
    return render_template('subjects.html')

@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    """Add student page"""
    return render_template('Add_students.html')

@app.route('/add-question', methods=['GET', 'POST'])
def Add_Question():
    """Add question page"""
    return render_template('Add_Question.html')

@app.route('/filter', methods=['GET', 'POST'])
def filter():
    """Filter page"""
    return render_template('filter.html')

@app.route('/search', methods=['GET'])
def search():
    """Search functionality"""
    query = request.args.get('q', '')
    return render_template('filter_result.html') if False else redirect(url_for('Home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def Register():
    """Register page"""
    return render_template('Register.html')

@app.route('/logout')
def logout():
    """Logout"""
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('Home'))

@app.route('/explore-technology')
def explore_technology():
    """Explore Technology topics"""
    return render_template('technology.html')

@app.route('/explore-programming-languages')
def explore_programing_lang():
    """Explore Programming Languages"""
    return render_template('programing_lang.html')

@app.route('/explore-computer-science')
def explore_computer_science():
    """Explore Computer Science"""
    return render_template('Computer_seience.html')

# ==================== AI QUIZ GENERATOR ROUTES ====================

@app.route('/ai-quiz-generator')
def ai_quiz_generator():
    """Display the AI Quiz Generator page"""
    return render_template('ai_quiz_generator.html')


@app.route('/api/generate-quiz', methods=['POST'])
def generate_quiz():
    """API endpoint to generate a quiz using AI"""
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        num_questions = int(data.get('num_questions', 5))
        difficulty = data.get('difficulty', 'intermediate')
        
        # Validate inputs
        if not topic:
            return jsonify({
                'success': False,
                'message': 'Topic is required'
            }), 400
        
        if num_questions < 1 or num_questions > 20:
            return jsonify({
                'success': False,
                'message': 'Number of questions must be between 1 and 20'
            }), 400
        
        # Initialize AI generator
        generator = AIQuizGenerator()
        
        # Generate quiz
        result = generator.generate_quiz(
            topic=topic,
            num_questions=num_questions,
            difficulty=difficulty
        )
        
        if result['success']:
            # Store in database
            conn = get_db()
            quiz_data_json = json.dumps(result['data'])
            
            cursor = conn.execute(
                """INSERT INTO ai_generated_quizzes 
                   (topic, difficulty, num_questions, quiz_data, created_by)
                   VALUES (?, ?, ?, ?, ?)""",
                (topic, difficulty, num_questions, quiz_data_json, 'user')
            )
            conn.commit()
            quiz_id = cursor.lastrowid
            
            return jsonify({
                'success': True,
                'quiz_id': quiz_id,
                'data': result['data'],
                'message': result['message']
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating quiz: {str(e)}'
        }), 500


@app.route('/ai-quiz/<int:quiz_id>')
def take_ai_quiz(quiz_id):
    """Display an AI-generated quiz for taking"""
    try:
        conn = get_db()
        quiz = conn.execute(
            'SELECT * FROM ai_generated_quizzes WHERE id = ?',
            (quiz_id,)
        ).fetchone()
        
        if not quiz:
            flash('Quiz not found', 'error')
            return redirect(url_for('ai_quiz_generator'))
        
        quiz_data = json.loads(quiz['quiz_data'])
        
        return render_template('take_ai_quiz.html', 
                             quiz_id=quiz_id,
                             quiz=quiz_data,
                             topic=quiz['topic'])
    except Exception as e:
        flash(f'Error loading quiz: {str(e)}', 'error')
        return redirect(url_for('ai_quiz_generator'))


@app.route('/api/submit-quiz/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    """Submit quiz answers and calculate score"""
    try:
        conn = get_db()
        quiz = conn.execute(
            'SELECT quiz_data FROM ai_generated_quizzes WHERE id = ?',
            (quiz_id,)
        ).fetchone()
        
        if not quiz:
            return jsonify({
                'success': False,
                'message': 'Quiz not found'
            }), 404
        
        data = request.get_json()
        student_name = data.get('student_name', 'Anonymous')
        user_answers = data.get('answers', {})
        
        quiz_data = json.loads(quiz['quiz_data'])
        questions = quiz_data.get('questions', [])
        
        # Calculate score
        score = 0
        results = []
        
        for q in questions:
            q_id = str(q.get('id'))
            correct_answer = q.get('correct_answer')
            user_answer = user_answers.get(q_id)
            
            is_correct = user_answer == correct_answer
            if is_correct:
                score += 1
            
            results.append({
                'question_id': q_id,
                'correct': is_correct,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'explanation': q.get('explanation', '')
            })
        
        # Store attempt in database
        conn.execute(
            """INSERT INTO ai_quiz_scores 
               (quiz_id, student_name, score, total_questions, user_answers)
               VALUES (?, ?, ?, ?, ?)""",
            (quiz_id, student_name, score, len(questions), json.dumps(user_answers))
        )
        conn.commit()
        
        percentage = (score / len(questions) * 100) if questions else 0
        
        return jsonify({
            'success': True,
            'score': score,
            'total': len(questions),
            'percentage': round(percentage, 2),
            'results': results,
            'message': f'Quiz submitted! You scored {score}/{len(questions)}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error submitting quiz: {str(e)}'
        }), 500


@app.route('/ai-quiz-history')
def quiz_history():
    """Display quiz history and scores"""
    try:
        conn = get_db()
        
        # Get all quizzes
        quizzes = conn.execute(
            'SELECT * FROM ai_generated_quizzes ORDER BY created_at DESC'
        ).fetchall()
        
        # Get scores for each quiz
        quiz_stats = []
        for quiz in quizzes:
            scores = conn.execute(
                'SELECT score, total_questions FROM ai_quiz_scores WHERE quiz_id = ?',
                (quiz['id'],)
            ).fetchall()
            
            quiz_info = {
                'id': quiz['id'],
                'topic': quiz['topic'],
                'difficulty': quiz['difficulty'],
                'num_questions': quiz['num_questions'],
                'created_at': quiz['created_at'],
                'total_attempts': len(scores),
                'average_score': 0
            }
            
            if scores:
                avg = sum(s['score'] for s in scores) / len(scores)
                quiz_info['average_score'] = round(avg, 2)
            
            quiz_stats.append(quiz_info)
        
        return render_template('ai_quiz_history.html', quizzes=quiz_stats)
    except Exception as e:
        flash(f'Error loading history: {str(e)}', 'error')
        return redirect(url_for('ai_quiz_generator'))


# ==================== PDF SUMMARIZER ROUTES ====================

@app.route('/pdf-summarizer')
def pdf_summarizer():
    """PDF Summarizer page"""
    return render_template('pdf_summarizer.html')


@app.route('/api/upload-pdf', methods=['POST'])
def upload_pdf():
    """Upload and process PDF file"""
    try:
        if 'pdf_file' not in request.files:
            return jsonify({'success': False, 'message': 'No PDF file provided'}), 400
        
        pdf_file = request.files['pdf_file']
        num_questions = int(request.form.get('num_questions', 5))
        
        if pdf_file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        if not pdf_file.filename.lower().endswith('.pdf'):
            return jsonify({'success': False, 'message': 'Please upload a PDF file'}), 400
        
        # Initialize PDF summarizer
        summarizer = PDFSummarizer()
        
        # Save uploaded file
        upload_folder = 'uploads'
        os.makedirs(upload_folder, exist_ok=True)
        pdf_path, success = summarizer.save_upload(pdf_file, upload_folder)
        
        if not success:
            return jsonify({'success': False, 'message': 'Failed to save PDF file'}), 500
        
        # Process PDF
        result = summarizer.process_pdf(pdf_path, num_questions)
        
        if result['success']:
            # Store in database
            conn = get_db()
            summary_data = result['data']['summary']
            questions_data = result['data']['questions']
            
            # Insert summary
            cursor = conn.execute(
                """INSERT INTO pdf_summaries 
                   (filename, original_filename, num_pages, num_questions, summary_text, key_points, 
                    topics, difficulty_level, upload_path, uploaded_by)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    os.path.basename(pdf_path),
                    pdf_file.filename,
                    result['data']['num_pages'],
                    num_questions,
                    summary_data.get('summary', ''),
                    json.dumps(summary_data.get('key_points', [])),
                    json.dumps(summary_data.get('topics', [])),
                    summary_data.get('difficulty_level', 'intermediate'),
                    pdf_path,
                    'user'
                )
            )
            summary_id = cursor.lastrowid
            
            # Insert questions
            for idx, question in enumerate(questions_data):
                conn.execute(
                    """INSERT INTO pdf_questions 
                       (summary_id, question, options, correct_answer, explanation, difficulty, question_index)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        summary_id,
                        question.get('question', ''),
                        json.dumps(question.get('options', [])),
                        question.get('correct_answer', ''),
                        question.get('explanation', ''),
                        question.get('difficulty', 'intermediate'),
                        idx
                    )
                )
            
            conn.commit()
            
            return jsonify({
                'success': True,
                'summary_id': summary_id,
                'data': result['data'],
                'message': result['message']
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error processing PDF: {str(e)}'
        }), 500


@app.route('/pdf-summary/<int:summary_id>')
def view_summary(summary_id):
    """View PDF summary and questions"""
    try:
        conn = get_db()
        
        # Get summary
        summary = conn.execute(
            'SELECT * FROM pdf_summaries WHERE id = ?',
            (summary_id,)
        ).fetchone()
        
        if not summary:
            flash('Summary not found', 'error')
            return redirect(url_for('pdf_summarizer'))
        
        # Get questions
        questions = conn.execute(
            'SELECT * FROM pdf_questions WHERE summary_id = ? ORDER BY question_index',
            (summary_id,)
        ).fetchall()
        
        # Parse JSON fields
        summary_data = dict(summary)
        summary_data['key_points'] = json.loads(summary['key_points'])
        summary_data['topics'] = json.loads(summary['topics'])
        
        questions_data = []
        for q in questions:
            q_dict = dict(q)
            q_dict['options'] = json.loads(q['options'])
            questions_data.append(q_dict)
        
        return render_template('view_summary.html', 
                             summary=summary_data,
                             questions=questions_data)
    except Exception as e:
        flash(f'Error loading summary: {str(e)}', 'error')
        return redirect(url_for('pdf_summarizer'))


@app.route('/api/submit-pdf-questions/<int:summary_id>', methods=['POST'])
def submit_pdf_questions(summary_id):
    """Submit answers to PDF-generated questions"""
    try:
        conn = get_db()
        data = request.get_json()
        student_name = data.get('student_name', 'Anonymous')
        user_answers = data.get('answers', {})
        
        # Get questions
        questions = conn.execute(
            'SELECT * FROM pdf_questions WHERE summary_id = ? ORDER BY question_index',
            (summary_id,)
        ).fetchall()
        
        if not questions:
            return jsonify({'success': False, 'message': 'No questions found'}), 404
        
        # Calculate score
        score = 0
        results = []
        
        for q in questions:
            q_id = str(q['id'])
            correct_answer = q['correct_answer']
            user_answer = user_answers.get(q_id)
            
            is_correct = user_answer == correct_answer
            if is_correct:
                score += 1
            
            # Record attempt
            conn.execute(
                """INSERT INTO pdf_question_attempts 
                   (question_id, student_name, user_answer, is_correct)
                   VALUES (?, ?, ?, ?)""",
                (q['id'], student_name, user_answer, 1 if is_correct else 0)
            )
            
            results.append({
                'question_id': q_id,
                'correct': is_correct,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'explanation': q['explanation']
            })
        
        conn.commit()
        
        percentage = (score / len(questions) * 100) if questions else 0
        
        return jsonify({
            'success': True,
            'score': score,
            'total': len(questions),
            'percentage': round(percentage, 2),
            'results': results,
            'message': f'Quiz submitted! You scored {score}/{len(questions)}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error submitting answers: {str(e)}'
        }), 500


@app.route('/pdf-summaries-list')
def pdf_summaries_list():
    """View list of all PDF summaries"""
    try:
        conn = get_db()
        
        summaries = conn.execute(
            'SELECT * FROM pdf_summaries ORDER BY created_at DESC'
        ).fetchall()
        
        summaries_data = []
        for s in summaries:
            s_dict = dict(s)
            s_dict['key_points'] = json.loads(s['key_points'])
            s_dict['topics'] = json.loads(s['topics'])
            
            # Count questions
            q_count = conn.execute(
                'SELECT COUNT(*) as count FROM pdf_questions WHERE summary_id = ?',
                (s['id'],)
            ).fetchone()['count']
            
            s_dict['num_questions'] = q_count
            summaries_data.append(s_dict)
        
        return render_template('pdf_summaries_list.html', summaries=summaries_data)
    except Exception as e:
        flash(f'Error loading summaries: {str(e)}', 'error')
        return redirect(url_for('pdf_summarizer'))


# ==================== MISSING ROUTES ====================

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page"""
    return "Forgot Password Feature Coming Soon"



@app.route('/images/<filename>')
def images(filename):
    """Serve images from IMAGES folder"""
    return send_from_directory('IMAGES', filename)


@app.route('/result', methods=['GET', 'POST'])
def Result():
    """Result page"""
    return render_template('Result.html') if False else "Result Page"


@app.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    """Verify email page"""
    return render_template('verify_email.html') if False else "Verify Email Page"


@app.route('/student/<int:Sr_no>')
def view_student(Sr_no):
    """View student details"""
    return render_template('view_student.html') if False else "View Student Page"


@app.route('/student/edit/<int:Sr_no>', methods=['GET', 'POST'])
def edit_student(Sr_no):
    """Edit student"""
    return render_template('edit_student.html') if False else "Edit Student Page"


@app.route('/student/delete/<int:Sr_no>')
def delete_candidate(Sr_no):
    """Delete student"""
    return redirect(url_for('students'))


# Quiz category routes
@app.route('/quiz/operating-system/<int:qno>')
@app.route('/quiz/operating-system')
def operating_system(qno=0):
    """Operating System quiz"""
    return render_template('Theory.html')

@app.route('/quiz/dbms/<int:qno>')
@app.route('/quiz/dbms')
def dbms_lang(qno=0):
    """DBMS quiz"""
    return render_template('Theory.html')

@app.route('/quiz/computer-networks/<int:qno>')
@app.route('/quiz/computer-networks')
def computer_network(qno=0):
    """Computer Networks quiz"""
    return render_template('Theory.html')

@app.route('/quiz/data-structures/<int:qno>')
@app.route('/quiz/data-structures')
def data_structure(qno=0):
    """Data Structures quiz"""
    return render_template('Theory.html')

@app.route('/quiz/c-lang/<int:qno>')
@app.route('/quiz/c-lang')
def c_lang(qno=0):
    """C Language quiz"""
    return render_template('c_lang.html')

@app.route('/quiz/cpp-lang/<int:qno>')
@app.route('/quiz/cpp-lang')
def cpp_lang(qno=0):
    """C++ Language quiz"""
    return render_template('cpp_lang.html')

@app.route('/quiz/java-lang/<int:qno>')
@app.route('/quiz/java-lang')
def java_lang(qno=0):
    """Java Language quiz"""
    return render_template('java_lang.html')

@app.route('/quiz/python-lang/<int:qno>')
@app.route('/quiz/python-lang')
def python_lang(qno=0):
    """Python Language quiz"""
    return render_template('python_lang.html')

@app.route('/quiz/web-development/<int:qno>')
@app.route('/quiz/web-development')
def web_development(qno=0):
    """Web Development quiz"""
    return render_template('Theory.html')

@app.route('/quiz/artificial-intelligence/<int:qno>')
@app.route('/quiz/artificial-intelligence')
def Artificial_Intelligence(qno=0):
    """Artificial Intelligence quiz"""
    return render_template('Artificial_Intelligence.html')

@app.route('/quiz/data-science/<int:qno>')
@app.route('/quiz/data-science')
def data_science(qno=0):
    """Data Science quiz"""
    return render_template('data_science.html')

@app.route('/quiz/cyber-security/<int:qno>')
@app.route('/quiz/cyber-security')
def cyber_security(qno=0):
    """Cyber Security quiz"""
    return render_template('cyber_security.html')

@app.route('/quiz/cloud-computing/<int:qno>')
@app.route('/quiz/cloud-computing')
def cloud_computing(qno=0):
    """Cloud Computing quiz"""
    return render_template('cloud_computing.html')

@app.route('/quiz/mobile-app-development/<int:qno>')
@app.route('/quiz/mobile-app-development')
def Mobile_App_Development(qno=0):
    """Mobile App Development quiz"""
    return render_template('mobile_app_development.html')


if __name__ == "__main__":
    
    app.run(debug=True)