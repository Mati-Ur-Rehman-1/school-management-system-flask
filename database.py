import psycopg2
from werkzeug.security import generate_password_hash


def connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="student",
        user="postgres",
        password="root"
    )


def create_table():
    conn = connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll_no VARCHAR(20) PRIMARY KEY,
            name VARCHAR(50),
            f_name VARCHAR(50),
            class_name VARCHAR(20),
            subject VARCHAR(20),
            grade VARCHAR(20)

        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


def create_user(username, email, password):
    conn = connection()
    cur = conn.cursor()

    hashed = generate_password_hash(password)

    cur.execute("""
            INSERT INTO users (username, email, password)
            VALUES (%s, %s, %s)
        """, (username, email, hashed))

    conn.commit()
    cur.close()
    conn.close()


def get_unique_classes():
    conn = connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT subject FROM students ORDER BY subject;")
    classes = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return classes


def filter_by_class(class_name):
    conn = connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM students WHERE subject = %s", (class_name,))
    students = cur.fetchall()

    cur.close()
    conn.close()
    return students



def get_user_by_email(email):
    conn = connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


def insert_student(roll_no, name, f_name, class_name, subject, grade):
    conn = connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO students (roll_no, name, f_name, class_name, subject, grade)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (roll_no, name, f_name, class_name, subject, grade))

    conn.commit()
    cur.close()
    conn.close()


def get_all_students():
    conn = connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows


def get_students_paginated(offset, limit):
    conn = connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM students
        ORDER BY roll_no
        LIMIT %s OFFSET %s
    """, (limit, offset))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def count_students():
    conn = connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM students")
    total = cur.fetchone()[0]

    cur.close()
    conn.close()
    return total


def filter_class_paginated(class_name, offset, limit):
    conn = connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM students 
        WHERE subject = %s
        ORDER BY roll_no
        LIMIT %s OFFSET %s
    """, (class_name, limit, offset))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def count_students_filtered(class_name):
    conn = connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) FROM students
        WHERE subject = %s
    """, (class_name,))

    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return total


def get_student(roll_no):
    conn = connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM students WHERE roll_no = %s", (roll_no,))
    student = cur.fetchone()

    cur.close()
    conn.close()
    return student


def update_student(roll_no, name, f_name, class_name, subject, grade):
    conn = connection()
    cur = conn.cursor()

    cur.execute("""
          UPDATE students
          SET name=%s, f_name=%s, class_name=%s, subject=%s, grade=%s
          WHERE roll_no=%s
      """, (name, f_name, class_name, subject, grade, roll_no))

    conn.commit()
    cur.close()
    conn.close()


def delete_student(roll_no):
    conn = connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE roll_no = %s", (roll_no,))
    conn.commit()

    cur.close()
    conn.close()
