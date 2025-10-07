import mysql.connector
from mysql.connector import errorcode
from tabulate import tabulate


DB_NAME = 'student_db'

# Connect to MySQL server (without specifying database)
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='nagasri@2004'  # Replace with your MySQL root password
)
cursor = conn.cursor()

# Create database if it doesn't exist
try:
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    print(f"Database '{DB_NAME}' is ready.")
except mysql.connector.Error as err:
    print(f"Failed creating database: {err}")
    exit(1)

# Now connect to the database
conn.database = DB_NAME

# Create table if it doesn't exist
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
print("Table 'students' is ready.")


# Student Class
class Student:
    def __init__(self, name, age, course, marks, attendance):
        self.name = name
        self.age = age
        self.course = course
        self.marks = marks
        self.attendance = attendance

# Functions
def add_student(student):
    query = "INSERT INTO students (name, age, course, marks, attendance) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (student.name, student.age, student.course, student.marks, student.attendance))
    conn.commit()
    print("Student added successfully!")

def update_student(student_id, field, value):
    query = f"UPDATE students SET {field} = %s WHERE id = %s"
    cursor.execute(query, (value, student_id))
    conn.commit()
    print("Student updated successfully!")

def delete_student(student_id):
    query = "DELETE FROM students WHERE id = %s"
    cursor.execute(query, (student_id,))
    conn.commit()
    print("Student deleted successfully!")

def search_student(student_id):
    query = "SELECT * FROM students WHERE id = %s"
    cursor.execute(query, (student_id,))
    result = cursor.fetchone()
    if result:
        print(tabulate([result], headers=["ID","Name","Age","Course","Marks","Attendance"]))
    else:
        print("Student not found!")

def view_all_students():
    query = "SELECT * FROM students"
    cursor.execute(query)
    result = cursor.fetchall()
    print(tabulate(result, headers=["ID","Name","Age","Course","Marks","Attendance"]))

# CLI Menu
def menu():
    while True:
        print("\n--- Student Management System ---")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. Search Student")
        print("5. View All Students")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Name: ")
            age = int(input("Age: "))
            course = input("Course: ")
            marks = int(input("Marks: "))
            attendance = int(input("Attendance %: "))
            student = Student(name, age, course, marks, attendance)
            add_student(student)
        elif choice == "2":
            student_id = int(input("Enter Student ID to update: "))
            field = input("Field to update (name/age/course/marks/attendance): ")
            value = input("Enter new value: ")
            if field in ["age", "marks", "attendance"]:
                value = int(value)
            update_student(student_id, field, value)
        elif choice == "3":
            student_id = int(input("Enter Student ID to delete: "))
            delete_student(student_id)
        elif choice == "4":
            student_id = int(input("Enter Student ID to search: "))
            search_student(student_id)
        elif choice == "5":
            view_all_students()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    menu()
