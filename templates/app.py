import flask

app = flask.Flask(__name__)
stud=[
    {
        'name':'Tanisha',
        'age':20,
    },
    {
        'name':' Smith',
        'age':22,
    },
    {
        'name':'Tejas',
        'age':19,
    },
    {
        'name':'Rama',
        'age':21,
    }
]
@app.route('/')
def Home():
    #create using html
    html = '<h1>Student List - for quiz competition</h1>'
    html += '<ul>'
    for student in stud:
        html += f"<li>Name: {student['name']}, Age: {student['age']}</li>"
    html += '</ul>'
    return html

@app.route('/about')
def about():
    return '<h1>About us</h1><p>This is the student management system</p>'

@app.route('/students')
def students():
    return """<h1>student list</h1><p>here is show the list of students , they are solve the Study quiz hub.</p>'
    <br>
    <a href="/">back to home</a>
    """

if __name__ == '__main__':
    app.run(debug=True)

    