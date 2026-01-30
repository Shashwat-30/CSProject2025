def validate_num(prompt, min_value=0, max_value=100):
    while True:
        try:
            value = float(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Please enter a number between {min_value} and {max_value}")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

students = []

def add_student():
    name = input("Enter student name: ")
    roll_number = input("Enter roll number: ").strip()
    student_class = input("Enter class: ").strip()

    marks = {}
    while True:
        subject = input("Enter subject name (or 'done' to finish): ").strip()
        if subject.lower() == 'done':
            break
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

    print("Student added successfully!")

def view_students():
    if not students:
        print("No students found.")
        return
    for idx, student in enumerate(students, 1):
        print(f"Student {idx}:")
        print(f"Name: {student['name']}")
        print(f"Roll number: {student['roll number']}")
        print(f"Class: {student['class']}")
        print("Marks:")
        for subject, mark in student['marks'].items():
            print(f"  {subject}: {mark}")
        print(f"Attendance: {student['attendance']}%")

def help_screen():
    print("Available commands:")
    print("1. add - Add a new student")
    print("2. view - View all students")
    print("3. help - Show this help screen")
    print("4. exit - Exit the program")

def menu():
    while True:
        help_screen()
        choice = input("Enter your choice: ")
        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            help_screen()
        elif choice == '4':
            print("Logging out ...")
            break
        else:
            print("Invalid choice! Please try again.")

users = {
    "admin": "admin123",
    "teacher": "teachpass"
}

def login():
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        if username in users and users[username] == password:
            print(f"WELCOME {username}!")
            menu()
            break
        else:
            print("Invalid credentials!")
            again = input("Do you want to login again? (yes/no): ").strip().lower()
            if again != "yes":
                print("Goodbye!")
                break

# Start the program
login()
