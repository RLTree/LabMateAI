import psycopg2
from psycopg2 import sql
import os


def create_tables(conn):
    """
    Create tables in the PostgreSQL database.
    """
    commands = [
        '''
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            user_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            department TEXT,
            role TEXT
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS tools (
            tool_id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            features TEXT,
            cost TEXT,
            description TEXT,
            url TEXT,
            language TEXT,
            platform TEXT
        )
        ''',
        '''
        CREATE TABLE IF NOT EXISTS interactions (
            interaction_id SERIAL PRIMARY KEY,
            user_id INTEGER,
            tool_id INTEGER,
            rating INTEGER,
            usage_frequency TEXT,
            timestamp TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(tool_id) REFERENCES tools(tool_id)
        )
        '''
    ]

    cursor = conn.cursor()
    for command in commands:
        cursor.execute(command)
    conn.commit()
    cursor.close()


def insert_sample_data(conn):
    """
    Insert sample data into the PostgreSQL database.
    """
    cursor = conn.cursor()

    # Insert sample users
    users = [
        ('Alice Johnson', 'alice@example.com', 'Biology', 'Researcher'),
        ('Bob Smith', 'bob@example.com', 'Chemistry', 'Student'),
        ('Charlie Davis', 'charlie@example.com', 'Physics', 'Professor')
    ]
    for user in users:
        cursor.execute('''
            INSERT INTO users (user_name, email, department, role)
            VALUES (%s, %s, %s, %s) ON CONFLICT (email) DO NOTHING
        ''', user)

    # Insert sample tools
    tools = [
        ('Seurat', 'Single-Cell Analysis', 'Single-cell RNA-seq;Clustering', 'Free',
         'An R package for single-cell RNA sequencing data.', 'https://satijalab.org/seurat/', 'R', 'Cross-platform'),
        ('Scanpy', 'Single-Cell Analysis', 'Single-cell RNA-seq;Visualization', 'Free',
         'A scalable toolkit for analyzing single-cell gene expression data.', 'https://scanpy.readthedocs.io/', 'Python', 'Cross-platform'),
        ('Bowtie', 'Genomics', 'Sequence Alignment;Genome Mapping', 'Free',
         'A fast and memory-efficient tool for aligning sequencing reads to long reference sequences.', 'https://bowtie-bio.sourceforge.net/index.shtml', 'C++', 'Cross-platform'),
        ('RNAAnalyzer', 'RNA', 'RNA-Seq Analysis;Differential Expression', 'Free',
         'A tool for analyzing RNA-Seq data and identifying differential gene expression.', 'https://rnaanalyzer.example.com/', 'R', 'Cross-platform')
    ]
    for tool in tools:
        cursor.execute('''
            INSERT INTO tools (name, category, features, cost, description, url, language, platform)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (name) DO NOTHING
        ''', tool)

    conn.commit()
    cursor.close()


def main():
    # Database connection parameters
    db_name = os.getenv('DB_NAME', 'labmate_db')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'password')
    db_host = os.getenv('DB_HOST', 'localhost')
    # Updated port for LabMateAI PostgreSQL server
    db_port = os.getenv('DB_PORT', '1357')

    # Connect to the PostgreSQL database
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return

    # Create tables
    create_tables(conn)
    # Insert sample data
    insert_sample_data(conn)

    # Close the connection
    conn.close()


if __name__ == "__main__":
    main()
