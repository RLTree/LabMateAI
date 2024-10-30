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
import sys
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Fetch the database URL
DATABASE_URL = os.getenv('DATABASE_URL')

# Initialize the connection pool
connection_pool = None  # Initialize as None

def get_connection_pool():
    global connection_pool
    if connection_pool is None:
        try:
            connection_pool = pool.SimpleConnectionPool(
                1, 20, DATABASE_URL
            )
            logging.debug("Initialized connection pool.")
        except Exception as e:
            logging.error("Error initializing connection pool: %s", e)
            raise e
    return connection_pool



def get_db_connection():
    """
    Gets a connection from the connection pool.

    Returns:
        psycopg2.extensions.connection: A database connection.

    Raises:
        psycopg2.Error: If an error occurs while getting a connection.
    """

    try:
        pool = get_connection_pool()
        conn = pool.getconn()
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


def get_engine(db_config, testing=False):
    """
    Creates a SQLAlchemy engine based on the provided database configuration.

    Args:
        db_config (dict): Database configuration with keys 'user', 'password', 'host', 'port', 'dbname'.
        testing (bool): If True, returns an in-memory SQLite engine.

    Returns:
        sqlalchemy.engine.Engine: The created SQLAlchemy engine.
    """
    if testing:
        try:
            engine = create_engine('sqlite:///:memory:')
            return engine
        except SQLAlchemyError as e:
            print(f"Failed to create SQLite in-memory engine: {e}")
            sys.exit(1)

    # Validate db_config
    required_keys = {'user', 'password', 'host', 'port', 'dbname'}
    if not db_config or not required_keys.issubset(db_config.keys()):
        print("Invalid database configuration. Required keys: 'user', 'password', 'host', 'port', 'dbname'.")
        sys.exit(1)

    # Construct the database URL
    try:
        url = (
            f"postgresql://{db_config['user']}:{db_config['password']}@"
            f"{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
        )
        engine = create_engine(url)
        return engine
    except SQLAlchemyError as e:
        print(f"Failed to create engine: {e}")
        sys.exit(1)
