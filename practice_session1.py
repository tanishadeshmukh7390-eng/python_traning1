#part-1 : List and Loop

Stud=['Tanisha','Tejash','Shubham','Sachin','Dhanashri']

marks=[100,60,45,90,95]

roll_no=[1001,1002,1003,1004,1005]

for i in Stud:
    print(Stud)
for i in marks:
    print(marks)
for i in roll_no:
    print(roll_no)


#part_2 : function
def get_status():
    if(marks<90):
        print("very good")
    elif(marks>70):
        print("good")
    elif(marks>35):
        print("need improvement")
    else:
        print("fail")

#part-3 : 



#step-1 : flask
import sqlite3
from flask import Flask ,flash ,rander_template ,request ,redirect ,url_for

app=Flask(__name__)
app.secret_key='Linkkiwi2026'

def get_db():
    conn=sqlite3.connect('project.db')
    conn.row_factory=sqlite3.Row
    return conn
def init_db():
    conn=get_db
    conn.execute()
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn= get_db()
    Stud=conn.execute('select *from')