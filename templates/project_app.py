from flask import Flask
app = Flask(__name__)
stud=[
    {
        'name':'John Doe',
        'age':20,
    },
    {
        'name':'Jane Smith',
        'age':22,
    },
    {
        'name':'Alice Johnson',
        'age':19,
    },
    {
        'name':'Bob Brown',
        'age':21,
    }
]

Quiz_Questions = [
    {
        "question": "What is Python?",
        "options": [
            "A) A high-level, interpreted programming language",
            "B) A type of snake",
            "C) A brand of computer",
            "D) A musical instrument"
        ],
    },
    {
        "question": "What is the use of Python?",
        "options": [
            "A) Web development",
            "B) Data analysis",
            "C) Artificial intelligence",
            "D) All of the above"
        ],
    },
    {
        "question": "What are the features of Python?",
        "options": [
            "A) Easy to learn and read",
            "B) Large standard library",
            "C) Dynamic typing",
            "D) All of the above"
        ],
    }
]

#2nd dictionary for quiz answers is created
answers = {
    1: "A",
    2: "D",
    3: "D"
}
@app.route('/')
def Home():
    return '<h1>****************************** STUDY MASTER PRO ****************************</h1><p>Welcome to the Study Master Pro! Here you can test your knowledge on various subjects through multiple-choice questions. Explore our subjects, take quizzes, and check your scores on the leaderboard. Get ready to challenge yourself and have fun learning!</p>'

@app.route('/about')
def about():
    return '<h1>About us</h1><p>This is a Study master pro(subject,MCQ,score,leaderboard).</p>'

@app.route('/students')
def students():
    #create using html
    html = '<h1>Student List - for Study Master Pro</h1>'
    html += '<ul>'
    for student in stud:
        html += f"<li>Name: {student['name']}, Age: {student['age']}</li>"
    html += '</ul>'
    return html

@app.route('/Subject')
def Subject():
    return '<h1>Subject</h1><p>Here is show the list of subjects for for mcq questions.</p><li>Python</li><li>java</li><li>c++</li><li>c</li>'

@app.route('/MCQ')
def MCQ():
    html = '<h1>MCQ</h1><p>Here is show the list of mcq questions for study quiz hub.</p>'
    html += '<ul>'
    score = 0
    question_no = 1
    for quiz in Quiz_Questions:
        html += f"<li>{quiz['question']}</li></br>"
        for option in quiz["options"]:
            html += f"<li><ol>{             option}</ol></li></br>"
            score = 0
        question_no += 1
    html += '</ul>'
    html += f'<p>Final Score: {score}</p>'
    return html

if __name__ == '__main__':
    app.run(debug=True)