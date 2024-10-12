# database.py

import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)


# Database connection parameters
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'labmate_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '1357')
}


def get_db_connection():
    """
    Establishes and returns a connection to the PostgreSQL database.

    Returns:
        psycopg2.connection: Database connection object.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logging.debug("Database connection established.")
        return conn
    except psycopg2.OperationalError as e:
        logging.error("Failed to connect to the database: %s", e)
        print("Failed to connect to the database. Please check your .env file and ensure that PostgreSQL is running.")
        raise e
