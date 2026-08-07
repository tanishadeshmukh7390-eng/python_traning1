#loop

Students=["John","Mary","Bob","Alice","sohan"]
list1=['ajay','vijay',12,True,3.12]

print("Display the Students List:")
print(Students[0])
print(Students[1])
print(Students[2])
print(Students[3])
print(Students[4])

print("Display the List1:")
print(list1[0])
print(list1[1])
print(list1[2])
print(list1[3])
print(list1[4])

for Student in Students:
    print(f"Hello {Student}!n Welcome to the class")

marks=[85,90,78,92,88]
for mark in marks:
    if mark>=90:
        print(f"Excellent! You scored {mark}.")
    elif mark>=80:
        print(f"Good job! You scored {mark}.")
    elif mark>=70:
        print(f"Fair effort! You scored {mark}.")
    else:
        print(f"Needs improvement. You scored {mark}.")

for i in range(1,11):
    print("the number is:",i)

for Student in range(0,6):
    print(f"Hello {Student}!n Welcome to the class")