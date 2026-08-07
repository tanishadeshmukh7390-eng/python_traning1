#Create a dictionary for a project quiz

#1st dictionary for quiz question and options is created

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

score = 0

question_no = 1

for quiz in Quiz_Questions:
    print(quiz["question"])

    for option in quiz["options"]:
        print(option)

    user_answer = input("Enter your answer: ")

    if user_answer.upper() == answers[question_no]:
        score += 1

    question_no += 1

print("Final Score:", score)

#Write a function 
#search_records(records,search_term)