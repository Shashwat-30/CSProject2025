# student.py

from utils import validate_num
import data  # Ensure data.py exists in the same directory, or create it if missing

def add_student(students):
    name = input("Enter student name: ")
    roll_number = input("Enter roll number: ").strip()

    # Prevent duplicate roll number
    if any(s['roll number'] == roll_number for s in students):
        print("A student with this roll number already exists!")
        return

    student_class = input("Enter class: ").strip()

    marks = {}
    while True:
        subject = input("Enter subject name (or 'done' to finish): ").strip()
        if subject.lower() == 'done':
            break
        if not subject:
            print("Subject name cannot be empty.")
            continue
        mark = validate_num(f"Enter marks for {subject}: ", 0, 100)
        marks[subject] = mark

    attendance = validate_num("Enter attendance percentage: ", 0, 100)

    students.append({
        "name": name,
        "roll number": roll_number,
        "class": student_class,
        "marks": marks,
        "attendance": attendance
    })

    data.save_data(students)
    print("Student added successfully!")

def view_students(students):
    if not students:
        print("No students found.")
        return
    for idx, student in enumerate(students, 1):
        print(f"\nStudent {idx}:")
        print(f"Name: {student['name']}")
        print(f"Roll number: {student['roll number']}")
        print(f"Class: {student['class']}")
        print("Marks:")
        print(f"{'Subject':<15}{'Marks':>10}")
        for subject, mark in student['marks'].items():
            print(f"{subject:<15}{mark:>10}")
        print(f"Attendance: {student['attendance']}%")
