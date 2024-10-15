# database.py
"""
This module manages database connections and creates SQLAlchemy engine instances.

Functions:
    get_db_connection: Gets a connection from the connection pool.
    release_db_connection: Releases a connection back to the pool.
    get_engine: Creates a SQLAlchemy engine using the provided database configuration.
"""
import os
import logging
import psycopg2
from psycopg2 import sql, pool
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Fetch the database URL
DATABASE_URL = os.getenv('DATABASE_URL')

# Initialize the connection pool
connection_pool = pool.SimpleConnectionPool(
    1, 20, DATABASE_URL
)


def get_db_connection():
    """
    Gets a connection from the connection pool.

    Returns:
        psycopg2.extensions.connection: A database connection.

    Raises:
        psycopg2.Error: If an error occurs while getting a connection.
    """

    try:
        conn = connection_pool.getconn()
        if conn:
            logging.debug("Acquired connection from pool.")
            return conn
    except psycopg2.Error as e:
        logging.error("Error getting connection from pool: %s", e)
        raise e


def release_db_connection(conn):
    """
    Releases a connection back to the pool.

    Args:
        conn (psycopg2.extensions.connection): The connection to release.
    """

    try:
        connection_pool.putconn(conn)
        logging.debug("Released connection back to pool.")
    except psycopg2.Error as e:
        logging.error("Error releasing connection to pool: %s", e)
        raise e


def get_engine(db_config):
    """
    Creates a SQLAlchemy engine using the provided database configuration.

    Args:
        db_config (dict): Database configuration parameters.

    Returns:
        Engine: A SQLAlchemy Engine instance.
    """
    try:
        database_url = f"postgresql://{db_config['user']}:{db_config['password']}@" \
            f"{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
        engine = create_engine(database_url)
        return engine
    except Exception as e:
        logging.error("Failed to create database engine: %s", e)
        raise e
