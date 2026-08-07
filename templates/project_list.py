'''Display the list of Questions in the project

Q1 = "Question 1: What is the python ?"
Q2 = "Question 2: What is the use of python ? "
Q3 = "Question 3: What are the features of python ? "
Q4 = "Question 4: What are the applications of python ? " 
Q5 = "Question 5: What are the advantages of python ? " 
Questions = ['Q1','Q2','Q3','Q4','Q5']

def Choose_answer():
    for i in range(len(Questions)):
        print(Questions[i])
    choice = int(input("Enter the question number : "))
    if choice == 1:
        print("Answer: A. A high-level, interpreted programming language")
    elif choice == 2:
        print("Answer: D. All of the above")
    elif choice == 3:
        print("Answer: D. All of the above")
    elif choice == 4:
        print("Answer: D. All of the above")
    elif choice == 5:
        print("Answer: D. All of the above")
    else:
        print("Invalid choice. Please select a valid question number.")

for i in range(0,5):
    Choose_answer()
    '''

Questions = ["Question 1: What is the python ?","Question 2: What is the use of python ? ","Question 3: What are the features of python ? ",
             "Question 4: What are the applications of python ? ","Question 5: What are the advantages of python ? " ]

Answers = []