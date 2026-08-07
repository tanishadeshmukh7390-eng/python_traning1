
from flask import Flask, render_template, request
import os
from groq import Groq

app = Flask(__name__, template_folder='day_ai_templates')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/get_tip', methods=['POST'])
def get_tip():
    student_name = request.form['name']
    student_username = request.form['username']
    student_email = request.form['email']
    student_subject = request.form['subject']

   

# Step 1 - Create a prompt.
    prompt = f"""
Student name: {student_name}
Student username: {student_username}
Student email: {student_email}
Subject: {student_subject}
Please provide practical study tips, it should not be more than 2 lines.
"""

# Step 2 - API call to Groq API to get the response.
    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role":"user",
         "content": prompt}
    ]
)

# Step 3 - Print the response.
    tip = response.choices[0].message.content

    return render_template('result.html', name=student_name, username=student_username, email=student_email, subject=student_subject, tip=tip)

if __name__ == '__main__':
    app.run(debug=True, port=5005)
    