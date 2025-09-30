"""
main.py - Integrated Student Result Management System
Supports: Students, Subjects, Exams, Marks, PDF Reports, ML Predictions
"""
# import nessesary modules
import os
import joblib
import pandas as pd
import mysql.connector as sqlconn
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import hashlib
import getpass

# Credentials
DB_CONFIG = {
    'host':'sql12.freesqldatabase.com',
    'database':'sql12800214',
    'user':'sql12800214',
    'password':'d9vxZmJWA1'
}
MODEL_PATH = r""    # Add 'best_exam4_predictor.pkl' path

# DATABASE Connection
def get_connection():
    return sqlconn.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        port=DB_CONFIG.get("port", 3306)
    )

try:
    DB = get_connection()
    CUR = DB.cursor()
    print("Connected to database.")
except Exception as e:
    print("DB connection failed:", e)
    DB, CUR = None, None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# CREATE TABLES, if not exist
def init_tables():

    # User Table
    CUR.execute( """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL
    )
    """)

    # Students Table
    CUR.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT PRIMARY KEY,
            sname VARCHAR(50),
            sclass VARCHAR(10),
            gender VARCHAR(10),
            house VARCHAR(20),
            attendance FLOAT
        )
    """)

    # Subjects Table
    CUR.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INT AUTO_INCREMENT PRIMARY KEY,
            subject_name VARCHAR(30)
        )
    """)

    # Exams Table
    CUR.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            exam_id INT AUTO_INCREMENT PRIMARY KEY,
            exam_name VARCHAR(30),
            max_written FLOAT,
            max_practical FLOAT
        )
    """)

    # Marks Table
    CUR.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            id INT,
            subject_id INT,
            exam_id INT,
            written FLOAT,
            practical FLOAT,
            total FLOAT,
            PRIMARY KEY (id, subject_id, exam_id),
            FOREIGN KEY (id) REFERENCES students(id) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
            FOREIGN KEY (exam_id) REFERENCES exams(exam_id) ON DELETE CASCADE
        )
    """)
    DB.commit()
    print("All tables ensured.")

init_tables()

# BASIC OPERATIONS

def add_teacher(username, password):
    try:
        sql = "INSERT INTO users (username,password_hash) VALUES (%s,%s)"
        CUR.execute(sql, (username, hash_password(password)))
        DB.commit()
        print("Teacher added.")
    except:
        print("Username already exists.")

def login():
    # If no users exist, force creating the first teacher
    CUR.execute("SELECT COUNT(*) FROM users")
    count = CUR.fetchone()[0]
    if count == 0:
        print("No teachers found in the system. Please create the first teacher account.")
        username = input("Choose a username: ").strip()
        password = getpass.getpass("Choose a password: ")
        add_teacher(username, password)
        print("First teacher account created. Please login now.")

    for attempt in range(3):  # Allow max 3 attempts
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ").strip()
        sql = "SELECT password_hash FROM users WHERE username=%s"
        CUR.execute(sql, (username,))
        row = CUR.fetchone()
        if not row:
            print("Invalid username.")
            continue
        if hash_password(password) == row[0]:
            print(f"Welcome, {username} (teacher)")
            return True
        else:
            print("Invalid password.")
    
    print("Too many failed attempts. Exiting...")
    return False

def insert_student():
    i = int(input("\nEnter ID: "))
    nm = input("Enter Name: ").upper()
    cl = input("Enter Class (e.g. XII-A): ").upper()
    g = input("Enter Gender: ").upper()
    h = input("Enter House: ").upper()
    att = float(input("Enter Attendance %: "))
    CUR.execute("INSERT INTO students VALUES (%s,%s,%s,%s,%s,%s)", (i,nm,cl,g,h,att))
    DB.commit()
    print("Student inserted.")

def insert_subject():
    subj = input("\nEnter Subject Name: ").upper()
    CUR.execute("INSERT INTO subjects (subject_name) VALUES (%s)", (subj,))
    DB.commit()
    print("Subject inserted.")

def insert_exam():
    ename = input("\nEnter Exam Name: ").upper()
    mw = float(input("Enter Max Written Marks: "))
    mp = float(input("Enter Max Practical Marks: "))
    CUR.execute("INSERT INTO exams (exam_name,exam_no,max_written,max_practical) VALUES (%s,%s,%s)", (ename,mw,mp))
    DB.commit()
    print("Exam inserted.")

def insert_marks():
    sid = int(input("\nEnter Student ID: "))

    subj_name = input("Enter Subject Name: ").strip().upper()
    CUR.execute("SELECT subject_id FROM subjects WHERE subject_name=%s", (subj_name,))
    subj = CUR.fetchone()
    if not subj:
        print("Subject not found.")
        return
    subj_id = subj[0]

    exam_name = input("Enter Exam Name: ").strip().upper()
    CUR.execute("SELECT exam_id,max_written,max_practical FROM exams WHERE exam_name=%s", (exam_name,))
    exam = CUR.fetchone()
    if not exam:
        print("Exam not found.")
        return
    exam_id,mw,mp = exam

    w = float(input(f"Enter Written Marks (out of {mw}): "))
    p = float(input(f"Enter Practical Marks (out of {mp}): "))
    total = w + p

    CUR.execute("INSERT INTO marks VALUES (%s,%s,%s,%s,%s,%s)", (sid,subj_id,exam_id,w,p,total))
    DB.commit()
    print("Marks inserted.")

def update_student():
    sid = int(input("\nEnter Student ID to update: "))
    field = input("Enter field to update (sname, sclass, gender, house, attendance): ")
    value = input("Enter new value: ").upper()
    if field == "attendance":
        value = float(value)
    sql = f"UPDATE students SET {field}=%s WHERE id=%s"
    CUR.execute(sql, (value, sid))
    DB.commit()
    print("Student updated.")

def delete_student():
    sid = int(input("\nEnter Student ID to delete: "))
    CUR.execute("DELETE FROM students WHERE id=%s", (sid,))
    DB.commit()
    print("Student deleted.")

def update_subject():
    sid = int(input("\nEnter Subject ID to update: "))
    newname = input("Enter new subject name: ").upper()
    CUR.execute("UPDATE subjects SET subject_name=%s WHERE subject_id=%s", (newname, sid))
    DB.commit()
    print("Subject updated.")

def delete_subject():
    sid = int(input("\nEnter Subject ID to delete: "))
    CUR.execute("DELETE FROM subjects WHERE subject_id=%s", (sid,))
    DB.commit()
    print("Subject deleted.")

def update_exam():
    eid = int(input("\nEnter Exam ID to update: "))
    field = input("Enter field to update (exam_name, exam_no, max_written, max_practical): ")
    value = input("Enter new value: ").upper()
    if field in ("max_written", "max_practical", "exam_no"):
        value = float(value)
    sql = f"UPDATE exams SET {field}=%s WHERE exam_id=%s"
    CUR.execute(sql, (value, eid))
    DB.commit()
    print("Exam updated.")

def delete_exam():
    eid = int(input("\nEnter Exam ID to delete: "))
    CUR.execute("DELETE FROM exams WHERE exam_id=%s", (eid,))
    DB.commit()
    print("Exam deleted.")

def update_marks():
    sid = int(input("\nEnter Student ID: "))

    subj_name = input("Enter Subject Name: ").strip().upper()
    CUR.execute("SELECT subject_id FROM subjects WHERE subject_name=%s", (subj_name,))
    subj = CUR.fetchone()
    if not subj:
        print("Subject not found.")
        return
    subj_id = subj[0]

    exam_name = input("Enter Exam Name: ").strip().upper()
    CUR.execute("SELECT exam_id FROM exams WHERE exam_name=%s", (exam_name,))
    exam = CUR.fetchone()
    if not exam:
        print("Exam not found.")
        return
    exam_id = exam[0]

    field = input("Enter field to update (written, practical): ").strip().lower()
    if field not in ("written","practical"):
        print("Invalid field.")
        return
    value = float(input("Enter new value: "))

    CUR.execute(f"""
        UPDATE marks 
        SET {field}=%s, total=written+practical
        WHERE id=%s AND subject_id=%s AND exam_id=%s
    """,(value,sid,subj_id,exam_id))
    DB.commit()
    print("Marks updated.")

def delete_marks():
    sid = int(input("\nEnter Student ID: "))
    subj = int(input("Enter Subject ID: "))
    eid = int(input("Enter Exam ID: "))
    CUR.execute("DELETE FROM marks WHERE id=%s AND subject_id=%s AND exam_id=%s", (sid, subj, eid))
    DB.commit()
    print("Marks deleted.")

def show_table(name):
    CUR.execute(f"SELECT * FROM {name}")
    rows = CUR.fetchall()
    cols = [c[0] for c in CUR.description]
    print(" | ".join(cols))
    for r in rows:
        print(r)

# PDF REPORT
def generate_report(student_id):

    # Get student info
    CUR.execute("SELECT * FROM students WHERE id=%s", (student_id,))
    student = CUR.fetchone()
    if not student:
        print("Student not found.")
        return
    sid, sname, sclass, gender, house, att = student

    # Get marks joined with subjects and exams
    CUR.execute("""
        SELECT sub.subject_name, e.exam_no, e.exam_name,
               m.written, m.practical, m.total,
               (e.max_written+e.max_practical) as max_total
        FROM marks m
        JOIN subjects sub ON m.subject_id=sub.subject_id
        JOIN exams e ON m.exam_id=e.exam_id
        WHERE m.id=%s
        ORDER BY sub.subject_name, e.exam_no
    """, (student_id,))
    rows = CUR.fetchall()
    if not rows:
        print("No marks found.")
        return

    # Build DataFrame
    df = pd.DataFrame(rows, columns=["subject","exam_no","exam","written","practical","total","max_total"])
    df["percent"] = (df["total"]/df["max_total"]*100).round(2)

    # Pivot: subjects as rows, exams as column groups 
    pivot = df.pivot(index="subject", columns="exam_no", values=["written","practical","percent"])
    pivot = pivot.sort_index(axis=1, level=1)  
    pivot = pivot.reorder_levels([1,0], axis=1)  
    pivot = pivot.sort_index(axis=1, level=0)   
    pivot = pivot[[col for col in pivot.columns if col[1] in ["written","practical","percent"]]]
    pivot.columns = [f"Exam{exam}_{metric}" for exam,metric in pivot.columns]
    table_data = pivot.reset_index().round(1).values.tolist()
    col_labels = ["Subject"] + list(pivot.columns)

    # Chart data
    subjects = df["subject"].unique()
    exams = sorted(df["exam_no"].unique())
    marks_matrix = {sub: [] for sub in subjects}
    for ex in exams:
        for sub in subjects:
            val = df[(df["subject"]==sub) & (df["exam_no"]==ex)]["percent"]
            marks_matrix[sub].append(float(val.iloc[0]) if not val.empty else 0)

    # Plot PDF
    x = np.arange(len(subjects))
    width = 0.2
    filename = f"{sname}_report.pdf"
    with PdfPages(filename) as pdf:
        fig, (ax1, ax2) = plt.subplots(2,1,figsize=(12,11))
        ax1.axis("off")
        ax1.text(0.5,1.02,"REPORT CARD",ha="center",fontsize=16,fontweight="bold")
        ax1.text(0.02,0.95,f"Name: {sname}",fontsize=10,fontweight="bold")
        ax1.text(0.02,0.91,f"Class: {sclass}",fontsize=10,fontweight="bold")
        ax1.text(0.02,0.87,f"Gender: {gender}",fontsize=10,fontweight="bold")
        ax1.text(0.02,0.83,f"House: {house}",fontsize=10,fontweight="bold")
        ax1.text(0.02,0.79,f"Attendance: {att}%",fontsize=10,fontweight="bold")

        table = ax1.table(cellText=table_data,colLabels=col_labels,loc="center",cellLoc="center")
        table.auto_set_font_size(False); table.set_fontsize(8); table.scale(1.2,1.2)

        for i, ex in enumerate(exams):
            vals=[marks_matrix[sub][i] for sub in subjects]
            ax2.bar(x+i*width-width*len(exams)/2,vals,width,label=f"Exam{ex}")

        ax2.set_xticks(x); ax2.set_xticklabels(subjects,rotation=30,ha="right")
        ax2.set_ylabel("% Marks"); ax2.set_title("Performance Across Exams")
        ax2.legend()

        pdf.savefig(fig); plt.close(fig)

    print(f"Report generated: {filename}")



# MODEL Call
def load_model():
    if not os.path.exists(MODEL_PATH):
        print("Model file not found.")
        return None
    model=joblib.load(MODEL_PATH)
    print("Model loaded.")
    return model

# Predict marks
def predict_final_exam(student_id):
    model = load_model()
    if model is None:
        return

    # Get attendance
    CUR.execute("SELECT attendance FROM students WHERE id=%s",(student_id,))
    att = CUR.fetchone()
    if not att:
        print("No student found.")
        return
    attendance = float(att[0])

    # Get subjects 
    CUR.execute("SELECT subject_id, subject_name FROM subjects ORDER BY subject_id")
    subject_rows = CUR.fetchall()
    subjects = [sname for _, sname in subject_rows]

    # Get marks of exams 1–3 for all subjects (percentages)
    CUR.execute("""
        SELECT m.subject_id, e.exam_no, m.total/(e.max_written+e.max_practical)*100
        FROM marks m
        JOIN exams e ON m.exam_id = e.exam_id
        WHERE m.id=%s AND e.exam_no IN (1,2,3)
        ORDER BY m.subject_id, e.exam_no
    """,(student_id,))
    rows = CUR.fetchall()
    if not rows:
        print("No exam data found.")
        return

    # Build features in correct order
    features = [attendance]
    for exam_no in (1,2,3):
        for sid,_ in subject_rows:
            val = [perc for subj,ex,perc in rows if subj==sid and ex==exam_no]
            features.append(val[0] if val else 0)

    # Predict
    pred = model.predict([features])[0]

    print("Predicted Exam4 (Final) Marks:")
    for sub,val in zip(subjects, pred):
        print(f" - {sub.upper()}: {round(val,2)}")

# ---------------------------
# MENU
# ---------------------------
def main_menu():
    while True:
        try:
            print("\n" + "="*30)
            print("      STUDENT RESULT SYSTEM")
            print("="*30)
            print("1. Insert Data")
            print("2. Update Data")
            print("3. Delete Data")
            print("4. Show Data")
            print("5. Generate PDF Report")
            print("6. Predict Marks (predict percentage for final exam.)")
            print("7. Exit")
            print("="*30)
            choice = input("Choose an option (1-7): ").strip()

            if choice == "1":
                print("\n--- Insert Data ---")
                print("a. Student")
                print("b. Subject")
                print("c. Exam")
                print("d. Marks")
                sub_choice = input("Insert (a-d): ").strip().lower()
                if sub_choice == "a":
                    while True:
                        insert_student()
                        more = input("Add another student? (y/n): ").strip().lower()
                        if more != "y":
                            break
                elif sub_choice == "b":
                    while True:
                        insert_subject()
                        more = input("Add another subject? (y/n): ").strip().lower()
                        if more != "y":
                            break
                elif sub_choice == "c":
                    while True:
                        insert_exam()
                        more = input("Add another exam? (y/n): ").strip().lower()
                        if more != "y":
                            break
                elif sub_choice == "d":
                    while True:
                        insert_marks()
                        more = input("Add another marks entry? (y/n): ").strip().lower()
                        if more != "y":
                            break
                else:
                    print("Invalid.")


            elif choice == "2":
                print("\n--- Update Data ---")
                print("a. Student")
                print("b. Subject")
                print("c. Exam")
                print("d. Marks")
                sub_choice = input("Update (a-d): ").strip().lower()
                if sub_choice == "a": update_student()
                elif sub_choice == "b": update_subject()
                elif sub_choice == "c": update_exam()
                elif sub_choice == "d": update_marks()
                else: print("Invalid.")

            elif choice == "3":
                print("\n--- Delete Data ---")
                print("a. Student")
                print("b. Subject")
                print("c. Exam")
                print("d. Marks")
                sub_choice = input("Delete (a-d): ").strip().lower()
                if sub_choice == "a": delete_student()
                elif sub_choice == "b": delete_subject()
                elif sub_choice == "c": delete_exam()
                elif sub_choice == "d": delete_marks()
                else: print("Invalid.")

            elif choice == "4":
                print("\n--- Show Data ---")
                print("a. Students")
                print("b. Subjects")
                print("c. Exams")
                print("d. Marks")
                sub_choice = input("Show (a-d): ").strip().lower()
                if sub_choice == "a": show_table("students")
                elif sub_choice == "b": show_table("subjects")
                elif sub_choice == "c": show_table("exams")
                elif sub_choice == "d": show_table("marks")
                else: print("Invalid.")

            elif choice == "5":
                print("\n--- Generate PDF Report ---")
                sid = int(input("Enter Student ID: "))
                generate_report(sid)

            elif choice == "7":
                print("exiting......")
                break

            elif choice == "6":
                print('''!DISCLAIMER: available only for class XI and XII students.
                Only if the marks of all three exams are available.''')
                ch = input("Do you want to continue(y/n):")
                if ch == 'y':
                    sid = int(input("Enter Student ID: "))
                    predict_final_exam(sid)

            else:
                print("Invalid option. Please choose between 1-7.")
        
        except Exception as e:
            print("Error:", e)

if __name__=="__main__":
    if login():

        main_menu()
