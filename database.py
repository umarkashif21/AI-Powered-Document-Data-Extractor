# database.py
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

# --- Database Configuration ---
# IMPORTANT: Replace with your actual PostgreSQL credentials
DB_CONFIG = {
    "host": "localhost",
    "database": "psx_data",  # Using your existing database
    "user": "psx_user",      # Using your existing user
    "password": "fahadnadeem" # Using your existing password
}

def get_db_connection():
    """Establishes and returns a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Database connection established successfully.")
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        # In a real application, you'd handle this more gracefully,
        # perhaps by exiting or logging the error.
        raise

def create_resumes_table():
    """Creates the 'resumes' table if it doesn't already exist."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                id SERIAL PRIMARY KEY,
                file_name VARCHAR(255) NOT NULL,
                extracted_name VARCHAR(255),
                extracted_email VARCHAR(255),
                extracted_phone VARCHAR(50),
                extracted_skills TEXT, -- Storing as comma-separated string for simplicity
                full_text TEXT,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("Table 'resumes' ensured to exist.")
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()

def insert_resume_data(file_name, name, email, phone, skills, full_text):
    """Inserts extracted resume data into the 'resumes' table."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO resumes (file_name, extracted_name, extracted_email, extracted_phone, extracted_skills, full_text)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (file_name, name, email, phone, skills, full_text))
        conn.commit()
        print(f"Data for '{file_name}' inserted successfully.")
    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    # This block runs only when database.py is executed directly
    # It will ensure the table exists when you first run it.
    create_resumes_table()