# db_init.py

import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()

# Database connection parameters
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'labmate_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '1357')
}


def initialize_database():
    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Create users table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                user_name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                department VARCHAR(100),
                role VARCHAR(50)
            );
        """)

        # Create tools table if it doesn't exist (example)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tools (
                tool_id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(100),
                features TEXT,
                cost VARCHAR(50),
                description TEXT,
                url VARCHAR(255),
                language VARCHAR(50),
                platform VARCHAR(50)
            );
        """)

        # Commit the table creations
        conn.commit()

        # Identify the sequence associated with user_id
        cursor.execute("""
            SELECT pg_get_serial_sequence('users', 'user_id');
        """)
        sequence_name = cursor.fetchone()[0]
        print(f"Sequence identified: {sequence_name}")

        # Get the current maximum user_id
        cursor.execute("""
            SELECT COALESCE(MAX(user_id), 100000) FROM users;
        """)
        max_user_id = cursor.fetchone()[0]
        print(f"Current maximum user_id: {max_user_id}")

        # Set the sequence to the current maximum user_id
        # Setting is_called to False ensures nextval() returns max_user_id + 1
        cursor.execute(sql.SQL("SELECT setval(%s, %s, false);"),
                       [sequence_name, max_user_id])
        print(f"Sequence {sequence_name} set to {max_user_id}")

        # Commit the sequence adjustment
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()
        print("Database initialized successfully.")

    except (psycopg2.DatabaseError, psycopg2.OperationalError) as e:
        print(f"Database error: {e}")
        sys.exit(1)
    except (psycopg2.Error, KeyError, TypeError) as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    initialize_database()
