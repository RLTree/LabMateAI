# labmateai/data_loader.py

"""
This module contains functions for loading tool, user, and interaction data from the PostgreSQL database.
It ensures that each Tool instance includes a unique tool_id and handles data validation.
"""

import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from .tool import Tool

# Load environment variables from .env file in development
load_dotenv()

# Database connection string (Pulled from environment variables)
DATABASE_URL = os.getenv('DATABASE_URL')


def load_tools_from_db():
    """
    Loads tools from the PostgreSQL database.

    Returns:
        list: A list of Tool instances.

    Raises:
        RuntimeError: If there's an error connecting to the database or querying data.
    """
    tools = []

    try:
        # Establish a connection to the PostgreSQL database using a context manager
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cursor:
                # Execute SQL query to get tool data
                query = sql.SQL("""
                    SELECT tool_id, name, category, features, cost, description, url, language, platform
                    FROM tools;
                """)
                cursor.execute(query)

                # Fetch all tool records
                rows = cursor.fetchall()

                # Iterate over each record and create Tool instances
                for row in rows:
                    tool_id, name, category, features, cost, description, url, language, platform = row

                    # Convert features string to list
                    features_list = [feature.strip().lower(
                    ) for feature in features.split(';') if feature.strip()]

                    # Create Tool instance
                    tool = Tool(
                        tool_id=tool_id,
                        name=name,
                        category=category,
                        features=features_list,
                        cost=cost,
                        description=description,
                        url=url,
                        language=language,
                        platform=platform
                    )
                    tools.append(tool)

    except (Exception, psycopg2.DatabaseError) as e:
        raise RuntimeError(f"Error loading tools from the database:{e}") from e

    return tools


def load_users_from_db():
    """
    Loads user data from the PostgreSQL database.

    Returns:
        list: A list of dictionaries representing users.

    Raises:
        RuntimeError: If there's an error connecting to the database or querying data.
    """
    users = []

    try:
        # Establish a connection to the PostgreSQL database using a context manager
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cursor:
                # Execute SQL query to get user data
                query = sql.SQL("""
                    SELECT user_id, user_name, email, department, role
                    FROM users;
                """)
                cursor.execute(query)

                # Fetch all user records
                rows = cursor.fetchall()

                # Iterate over each record to create user dictionaries
                for row in rows:
                    user_id, user_name, email, department, role = row
                    user = {
                        'user_id': user_id,
                        'user_name': user_name,
                        'email': email,
                        'department': department,
                        'role': role
                    }
                    users.append(user)

    except (Exception, psycopg2.DatabaseError) as e:
        raise RuntimeError(f"Error loading users from the database: {e}") from e

    return users


def load_interactions_from_db():
    """
    Loads interaction data from the PostgreSQL database.

    Returns:
        list: A list of dictionaries representing interactions.

    Raises:
        RuntimeError: If there's an error connecting to the database or querying data.
    """
    interactions = []

    try:
        # Establish a connection to the PostgreSQL database using a context manager
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cursor:
                # Execute SQL query to get interaction data
                query = sql.SQL("""
                    SELECT interaction_id, user_id, tool_id, rating, usage_frequency, timestamp
                    FROM interactions;
                """)
                cursor.execute(query)

                # Fetch all interaction records
                rows = cursor.fetchall()

                # Iterate over each record to create interaction dictionaries
                for row in rows:
                    interaction_id, user_id, tool_id, rating, usage_frequency, timestamp = row
                    interaction = {
                        'interaction_id': interaction_id,
                        'user_id': user_id,
                        'tool_id': tool_id,
                        'rating': rating,
                        'usage_frequency': usage_frequency,
                        'timestamp': timestamp
                    }
                    interactions.append(interaction)

    except (Exception, psycopg2.DatabaseError) as e:
        raise RuntimeError(f"Error loading interactions from the database: {e}") from e

    return interactions
