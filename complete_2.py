"""
main.py - Integrated Student Result Management System
Supports: Students, Subjects, Exams, Marks, PDF Reports, ML Predictions
"""
# Jaruri modules
import os
import joblib
import pandas as pd
import mysql.connector as sqlconn
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# Khali mat chhodna
DB_CONFIG = {
    'host':'sql12.freesqldatabase.com',
    'database':'sql12800214',
    'user':'sql12800214',
    'password':'d9vxZmJWA1'
}
MODEL_PATH = r"D:\Python\CSProject2025\best_exam4_predictor.pkl"

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
    print("✅ Connected to database.")
except Exception as e:
    print("❌ DB connection failed:", e)
    DB, CUR = None, None

# CREATE TABLES, agar nhi hai toh!
def init_tables():
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

    CUR.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INT AUTO_INCREMENT PRIMARY KEY,
            subject_name VARCHAR(30)
        )
    """)

    CUR.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            exam_id INT AUTO_INCREMENT PRIMARY KEY,
            exam_name VARCHAR(30),
            exam_no INT,
            max_written FLOAT,
            max_practical FLOAT
        )
    """)

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
    print("✅ All tables ensured.")

init_tables()

# BASIC OPERATIONS
def insert_student():
    i = int(input("Enter ID: "))
    nm = input("Enter Name: ").upper()
    cl = input("Enter Class (e.g. XII-A): ").upper()
    g = input("Enter Gender: ").upper()
    h = input("Enter House: ").upper()
    att = float(input("Enter Attendance %: "))
    CUR.execute("INSERT INTO students VALUES (%s,%s,%s,%s,%s,%s)", (i,nm,cl,g,h,att))
    DB.commit()
    print("✅ Student inserted.")

def insert_subject():
    subj = input("Enter Subject Name: ").upper()
    CUR.execute("INSERT INTO subjects (subject_name) VALUES (%s)", (subj,))
    DB.commit()
    print("✅ Subject inserted.")

def insert_exam():
    ename = input("Enter Exam Name: ").upper()
    eno = int(input("Enter Exam Number (1-4): "))
    mw = float(input("Enter Max Written Marks: "))
    mp = float(input("Enter Max Practical Marks: "))
    CUR.execute("INSERT INTO exams (exam_name,exam_no,max_written,max_practical) VALUES (%s,%s,%s,%s)", (ename,eno,mw,mp))
    DB.commit()
    print("✅ Exam inserted.")

def insert_marks():
    sid = int(input("Enter Student ID: "))
    subj_id = int(input("Enter Subject ID: "))
    exam_id = int(input("Enter Exam ID: "))
    w = float(input("Enter Written Marks: "))
    p = float(input("Enter Practical Marks: "))
    CUR.execute("SELECT max_written,max_practical FROM exams WHERE exam_id=%s",(exam_id,))
    exam = CUR.fetchone()
    if not exam:
        print("❌ Exam not found.")
        return
    total = w+p
    CUR.execute("INSERT INTO marks VALUES (%s,%s,%s,%s,%s,%s)", (sid,subj_id,exam_id,w,p,total))
    DB.commit()
    print("✅ Marks inserted.")

def update_student():
    sid = int(input("Enter Student ID to update: "))
    field = input("Enter field to update (sname, sclass, gender, house, attendance): ")
    value = input("Enter new value: ").upper()
    if field == "attendance":
        value = float(value)
    sql = f"UPDATE students SET {field}=%s WHERE id=%s"
    CUR.execute(sql, (value, sid))
    DB.commit()
    print("✅ Student updated.")

def delete_student():
    sid = int(input("Enter Student ID to delete: "))
    CUR.execute("DELETE FROM students WHERE id=%s", (sid,))
    DB.commit()
    print("✅ Student deleted.")

def update_subject():
    sid = int(input("Enter Subject ID to update: "))
    newname = input("Enter new subject name: ").upper()
    CUR.execute("UPDATE subjects SET subject_name=%s WHERE subject_id=%s", (newname, sid))
    DB.commit()
    print("✅ Subject updated.")

def delete_subject():
    sid = int(input("Enter Subject ID to delete: "))
    CUR.execute("DELETE FROM subjects WHERE subject_id=%s", (sid,))
    DB.commit()
    print("✅ Subject deleted.")

def update_exam():
    eid = int(input("Enter Exam ID to update: "))
    field = input("Enter field to update (exam_name, exam_no, max_written, max_practical): ")
    value = input("Enter new value: ").upper()
    if field in ("max_written", "max_practical", "exam_no"):
        value = float(value)
    sql = f"UPDATE exams SET {field}=%s WHERE exam_id=%s"
    CUR.execute(sql, (value, eid))
    DB.commit()
    print("✅ Exam updated.")

def delete_exam():
    eid = int(input("Enter Exam ID to delete: "))
    CUR.execute("DELETE FROM exams WHERE exam_id=%s", (eid,))
    DB.commit()
    print("✅ Exam deleted.")

def update_marks():
    sid = int(input("Enter Student ID: "))
    subj = int(input("Enter Subject ID: "))
    eid = int(input("Enter Exam ID: "))
    field = input("Enter field to update (written, practical): ")
    value = float(input("Enter new value: "))

    CUR.execute(f"UPDATE marks SET {field}=%s, total=written+practical WHERE id=%s AND subject_id=%s AND exam_id=%s",
                (value, sid, subj, eid))
    DB.commit()
    print("✅ Marks updated.")

def delete_marks():
    sid = int(input("Enter Student ID: "))
    subj = int(input("Enter Subject ID: "))
    eid = int(input("Enter Exam ID: "))
    CUR.execute("DELETE FROM marks WHERE id=%s AND subject_id=%s AND exam_id=%s", (sid, subj, eid))
    DB.commit()
    print("✅ Marks deleted.")


def show_table(name):
    CUR.execute(f"SELECT * FROM {name}")
    rows = CUR.fetchall()
    cols = [c[0] for c in CUR.description]
    print(" | ".join(cols))
    for r in rows:
        print(r)

# PDF REPORT, tanmay bhai mst code tha bss thoda sa hi change kiya hu
def generate_report(student_id):
    # Get profile
    CUR.execute("SELECT * FROM students WHERE id=%s",(student_id,))
    student = CUR.fetchone()
    if not student:
        print("❌ Student not found.")
        return
    sid,sname,sclass,gender,house,att = student

    # Get marks with subjects+exams
    CUR.execute("""
        SELECT sub.subject_name, e.exam_name, m.written, m.practical, m.total,
               (e.max_written+e.max_practical) as max_total, e.exam_no
        FROM marks m
        JOIN subjects sub ON m.subject_id=sub.subject_id
        JOIN exams e ON m.exam_id=e.exam_id
        WHERE m.id=%s
        ORDER BY sub.subject_name, e.exam_no
    """,(student_id,))
    rows = CUR.fetchall()
    if not rows:
        print("No marks found for this student.")
        return

    # Convert to DataFrame
    cols = ["subject","exam","written","practical","total","max_total","exam_no"]
    df = pd.DataFrame(rows, columns=cols)
    df["percent"] = (df["total"]/df["max_total"]*100).round(2)

    # Pivot: subjects as rows, exams as column groups (Written/Practical/%)
    pivot = df.pivot(index="subject", columns="exam", values=["written","practical","percent"])
    pivot = pivot.sort_index(axis=1, level=1)  # exams in order
    pivot.columns = [f"{exam}_{metric}" for metric, exam in pivot.columns]
    table_data = pivot.reset_index().round(1).values.tolist()
    col_labels = ["Subject"] + list(pivot.columns)

    # Prepare chart data
    subjects = list(df["subject"].unique())
    exams = sorted(df["exam"].unique(), key=lambda e: df[df["exam"]==e]["exam_no"].iloc[0])
    marks_matrix = {sub: [] for sub in subjects}
    for ename in exams:
        for sub in subjects:
            val = df[(df["subject"]==sub) & (df["exam"]==ename)]["percent"]
            marks_matrix[sub].append(float(val.iloc[0]) if not val.empty else 0)

    x = np.arange(len(subjects))
    width = 0.15

    # CREATE PDF
    filename=f"{sname}_report.pdf"
    with PdfPages(filename) as pdf:
        fig,(ax1,ax2)=plt.subplots(2,1,figsize=(12,11))
        ax1.axis("off")
        ax1.text(0.5,1.02,"REPORT CARD",ha="center",fontsize=16,fontweight="bold")
        ax1.text(0.02,0.95,f"Name: {sname}",fontsize=10)
        ax1.text(0.02,0.92,f"Class: {sclass}  Gender: {gender}  House: {house}",fontsize=10)
        ax1.text(0.02,0.89,f"Attendance: {att}%",fontsize=10)

        table=ax1.table(cellText=table_data,colLabels=col_labels,loc="center",cellLoc="center")
        table.auto_set_font_size(False); table.set_fontsize(8); table.scale(1.2,1.2)

        for i,ename in enumerate(exams):
            vals=[marks_matrix[sub][i] for sub in subjects]
            ax2.bar(x+i*width-width*len(exams)/2,vals,width,label=ename)

        ax2.set_xticks(x); ax2.set_xticklabels(subjects,rotation=30,ha="right")
        ax2.set_ylabel("% Marks")
        ax2.set_title("Performance Across Exams")
        ax2.legend()

        pdf.savefig(fig); plt.close(fig)

    print(f"✅ Report generated: {filename}")


# MODEL, in dono pe zada dhyan mt do abhi
def load_model():
    if not os.path.exists(MODEL_PATH):
        print("❌ Model file not found.")
        return None
    model=joblib.load(MODEL_PATH)
    print("✅ Model loaded.")
    return model

def predict_final_exam(student_id):
    """
    Predict Exam4 (Final) marks for all subjects of a student
    using Exam1-Exam3 performance + attendance with the saved ML model.
    """
    model = load_model()
    if model is None:
        return

    # Fetch student info
    CUR.execute("SELECT attendance FROM students WHERE id=%s", (student_id,))
    row = CUR.fetchone()
    if not row:
        print("❌ Student not found.")
        return
    attendance = row[0]

    # Fetch marks for first 3 exams
    CUR.execute("""
        SELECT sub.subject_name, e.exam_no, m.written, m.practical, e.max_written, e.max_practical
        FROM marks m
        JOIN subjects sub ON m.subject_id=sub.subject_id
        JOIN exams e ON m.exam_id=e.exam_id
        WHERE m.id=%s AND e.exam_no IN (1,2,3)
        ORDER BY sub.subject_name, e.exam_no
    """, (student_id,))
    rows = CUR.fetchall()
    if not rows:
        print("❌ No exam data found for this student.")
        return

    # Build feature dictionary
    data = {}
    for subj, exam_no, w, p, mw, mp in rows:
        total = (w or 0) + (p or 0)
        max_total = (mw or 0) + (mp or 0)
        perc = round((total / max_total) * 100, 2) if max_total else 0
        key = f"Exam{exam_no}_{subj.upper().replace(' ', '_')}"
        data[key] = perc

    # Add attendance
    data["attendance_pct"] = attendance

    # Create DataFrame for model
    Xnew = pd.DataFrame([data])
    Xnew = pd.get_dummies(Xnew)

    # Align columns with trained model
    model_features = model.feature_names_in_
    for col in model_features:
        if col not in Xnew:
            Xnew[col] = 0
    Xnew = Xnew[model_features]

    # Predict
    pred = model.predict(Xnew)[0]
    subjects = sorted(set(r[0] for r in rows))
    predictions = {subj: round(float(p), 2) for subj, p in zip(subjects, pred)}

    print("📊 Predicted Exam4 (Final) Marks:")
    for subj, val in predictions.items():
        print(f" - {subj}: {val}")

    return predictions


# ---------------------------
# MENU
# ---------------------------
def main_menu():
    while True:
        print("\n" + "="*30)
        print("      STUDENT RESULT SYSTEM")
        print("="*30)
        print("1. Insert Data")
        print("2. Update Data")
        print("3. Delete Data")
        print("4. Show Data")
        print("5. Generate PDF Report")
        print("6. Predict Marks (abhi isko please use mt krna)")
        print("7. Exit")
        print("="*30)
        choice = input("Choose an option (1-6): ").strip()

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
            print("Bye.")
            break

        elif choice == "6":
            sid = int(input("Enter Student ID: "))
            predict_final_exam(sid)


        else:
            print("Invalid option. Please choose between 1-6.")

if __name__=="__main__":
    main_menu()
