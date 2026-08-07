s1 = int(input("subject 1 marks: "))
s2 = int(input("subject 2 marks: "))
s3 = int(input("subject 3 marks: "))
total = s1 + s2 + s3
print("Total marks: ", total)
parcentage = (total / 300) * 100
print("Percentage: ", parcentage)
if parcentage >= 90:
    print("Grade: A")
elif parcentage >= 80:
    print("Grade: B")
elif parcentage >= 70:
    print("Grade: C")
elif parcentage >= 60:
    print("Grade: D")
else:
    print("Grade: F")
      