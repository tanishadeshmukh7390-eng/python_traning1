#this is the mini project of collage smart potal 
#Create a project for list college smart portal

Students=["John","Mary","Bob","Alice","sohan"]
Roll_no=[1001,1002,1003,1004,1005]
Marks=[85,90,78,92,88]
Attendance=[90,95,85,98,92]

Notice=[
    "Notice 1: Student will be informed internship is starting from 28th may 2026",
    "Notice 2: Student will be informed about the exam schedule on 1st june 2026",
    "Notice 3: Tis is the python internship for 3 months"
]

def Student_login():
    name=input("Enter your name: ")
    for i in range(len(Students)):
        if name==Students[i]:
            print("Login successful")
            print(f"Welcome {Students[i]}! Your roll number is {Roll_no[i]}.")
            return
    print("Login failed. Name not found.")
    
Student_login()