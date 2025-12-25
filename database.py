import psycopg2


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

create_table()

