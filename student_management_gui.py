import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# ------------------- Database Setup -------------------
DB_NAME = 'student_db'

# Connect to MySQL server
conn = mysql.connector.connect(
    host='localhost',
    user='root',             # Replace with your MySQL username
    password='nagasri@2004' # Replace with your MySQL password
)
cursor = conn.cursor()

# Create database if not exists
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
conn.database = DB_NAME

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    age INT,
    course VARCHAR(50),
    marks INT,
    attendance INT
)
""")

# ------------------- GUI Setup -------------------
root = Tk()
root.title("Student Management System")
root.geometry("800x500")

# ------------------- Functions -------------------
def refresh_tree():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM students")
    for student in cursor.fetchall():
        tree.insert('', END, values=student)

def add_student():
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()
    marks = marks_entry.get()
    attendance = attendance_entry.get()

    if not (name and age and course and marks and attendance):
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        cursor.execute(
            "INSERT INTO students (name, age, course, marks, attendance) VALUES (%s, %s, %s, %s, %s)",
            (name, int(age), course, int(marks), int(attendance))
        )
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully!")
        refresh_tree()
        clear_entries()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_student():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select Student", "Please select a student to update")
        return
    student_id = tree.item(selected)['values'][0]

    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()
    marks = marks_entry.get()
    attendance = attendance_entry.get()

    if not (name and age and course and marks and attendance):
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        cursor.execute(
            "UPDATE students SET name=%s, age=%s, course=%s, marks=%s, attendance=%s WHERE id=%s",
            (name, int(age), course, int(marks), int(attendance), student_id)
        )
        conn.commit()
        messagebox.showinfo("Success", "Student updated successfully!")
        refresh_tree()
        clear_entries()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_student():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select Student", "Please select a student to delete")
        return
    student_id = tree.item(selected)['values'][0]
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?")
    if confirm:
        cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
        conn.commit()
        refresh_tree()
        clear_entries()

def clear_entries():
    name_entry.delete(0, END)
    age_entry.delete(0, END)
    course_entry.delete(0, END)
    marks_entry.delete(0, END)
    attendance_entry.delete(0, END)

def select_student(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected)['values']
        name_entry.delete(0, END)
        name_entry.insert(END, values[1])
        age_entry.delete(0, END)
        age_entry.insert(END, values[2])
        course_entry.delete(0, END)
        course_entry.insert(END, values[3])
        marks_entry.delete(0, END)
        marks_entry.insert(END, values[4])
        attendance_entry.delete(0, END)
        attendance_entry.insert(END, values[5])

# ------------------- GUI Widgets -------------------
# Input Frame
frame = Frame(root)
frame.pack(pady=20)

Label(frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
name_entry = Entry(frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

Label(frame, text="Age").grid(row=0, column=2, padx=5, pady=5)
age_entry = Entry(frame)
age_entry.grid(row=0, column=3, padx=5, pady=5)

Label(frame, text="Course").grid(row=1, column=0, padx=5, pady=5)
course_entry = Entry(frame)
course_entry.grid(row=1, column=1, padx=5, pady=5)

Label(frame, text="Marks").grid(row=1, column=2, padx=5, pady=5)
marks_entry = Entry(frame)
marks_entry.grid(row=1, column=3, padx=5, pady=5)

Label(frame, text="Attendance").grid(row=2, column=0, padx=5, pady=5)
attendance_entry = Entry(frame)
attendance_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons
Button(frame, text="Add Student", command=add_student, bg="green", fg="white").grid(row=3, column=0, pady=10)
Button(frame, text="Update Student", command=update_student, bg="blue", fg="white").grid(row=3, column=1, pady=10)
Button(frame, text="Delete Student", command=delete_student, bg="red", fg="white").grid(row=3, column=2, pady=10)
Button(frame, text="Clear Fields", command=clear_entries, bg="orange", fg="white").grid(row=3, column=3, pady=10)

# Table Frame
table_frame = Frame(root)
table_frame.pack(pady=20)

columns = ("ID", "Name", "Age", "Course", "Marks", "Attendance")
tree = ttk.Treeview(table_frame, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(fill=BOTH, expand=True)

tree.bind("<ButtonRelease-1>", select_student)

# Initial load
refresh_tree()

root.mainloop()
