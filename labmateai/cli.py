# cli.py

"""
CLI module for LabMateAI.

This module provides the CLI class, which handles user interactions
and provides tool recommendations based on user input.
"""

import sys
import psycopg2
import pandas as pd
from datetime import datetime
from labmateai.recommender import Recommender, build_user_item_matrix
from labmateai.collaborative_recommender import CollaborativeRecommender
from labmateai.hybrid_recommender import HybridRecommender
from labmateai.tool import Tool
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)


class CLI:
    """
    Command-Line Interface for LabMateAI.
    """

    def __init__(self, db_config=None):
        """
        Initializes the CLI, but defers loading data and initializing recommenders.

        Args:
            db_config (dict): Database connection configuration.
        """
        self.db_config = db_config or {
            'dbname': 'labmate_db',
            'user': 'postgres',   # Update with your DB username
            'password': 'password',  # Update with your DB password
            'host': 'localhost',  # Update with your host if different
            'port': '1357'  # Default PostgreSQL port for LabMateAI
        }
        self.tools = None
        self.recommender = None
        self.cf_recommender = None
        self.hybrid_recommender = None
        self.data_loaded = False

    def _get_or_create_user(self):
        """
        Handles user login or sign-up.
        """
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()

        print("\n--- LabMateAI User Login/Signup ---")
        email = input("Enter your email: ").strip().lower()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            print(f"Welcome back, {user[1]}.")
            user_id = user[0]
        else:
            print("No account found. Let's create a new one.")
            user_name = input("Enter your full name: ").strip()
            department = input("Enter your department: ").strip()
            role = input(
                "Enter your role (e.g., Researcher, Student): ").strip()

            cursor.execute("""
            INSERT INTO users (user_name, email, department, role)
            VALUES (%s, %s, %s, %s)
            RETURNING user_id
            """, (user_name, email, department, role))
            user_id = cursor.fetchone()[0]
            conn.commit()
            print(f"User successfully signed up! Welcome, {user_name}.")

        conn.close()
        return user_id

    def _log_interaction(self, user_id, tool_id, rating=None, usage_frequency=None):
        """
        Logs an interaction into the interactions table.

        Args:
            user_id (int): The ID of the user.
            tool_id (int): The ID of the tool.
            rating (int, optional): User rating for the tool (0-5).
            usage_frequency (str, optional): Frequency of tool usage.
        """
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()

        timestamp = datetime.now().isoformat()

        cursor.execute("""
        INSERT INTO interactions (user_id, tool_id, rating, usage_frequency, timestamp)
        VALUES (%s, %s, %s, %s, %s)
        """, (user_id, tool_id, rating, usage_frequency, timestamp))
        conn.commit()
        conn.close()

    def _load_data_and_initialize_recommenders(self):
        """
        Loads data and initializes the recommenders.
        """
        if not self.data_loaded:
            try:
                # Connect to the database
                conn = psycopg2.connect(**self.db_config)
                cursor = conn.cursor()

                # Load tools from the tools table
                cursor.execute("SELECT * FROM tools")
                tools_data = cursor.fetchall()
                if not tools_data:
                    raise RuntimeError("No tools found in the database.")

                self.tools = [
                    Tool(
                        tool_id=row[0],
                        name=row[1],
                        category=row[2],
                        features=[feature.strip().lower()
                                  for feature in row[3].split(';') if feature.strip()],
                        cost=row[4],
                        description=row[5],
                        url=row[6],
                        language=row[7],
                        platform=row[8]
                    )
                    for row in tools_data
                ]

                # Initialize the Recommender for content-based recommendations
                self.recommender = Recommender(tools=self.tools)

                # Load user-item interactions from the database
                cursor.execute(
                    "SELECT user_id, tool_id, rating FROM interactions WHERE rating IS NOT NULL")
                interactions_data = cursor.fetchall()

                if interactions_data:
                    interactions = pd.DataFrame(interactions_data, columns=[
                                                'user_id', 'tool_id', 'rating'])
                    logging.debug(f"Interactions DataFrame: \n{interactions}")

                    # Build user-item matrix
                    user_item_matrix = build_user_item_matrix(interactions)
                    logging.debug(f"User-item matrix: \n{user_item_matrix}")

                    # Initialize Collaborative Filtering Recommender
                    if not user_item_matrix.empty:
                        self.cf_recommender = CollaborativeRecommender(
                            user_item_matrix=user_item_matrix,
                            tools_df=pd.DataFrame(tools_data, columns=[
                                                  'tool_id', 'name', 'category', 'features', 'cost', 'description', 'url', 'language', 'platform']),
                            n_neighbors=5
                        )

                        # Initialize Hybrid Recommender
                        self.hybrid_recommender = HybridRecommender(
                            content_recommender=self.recommender,
                            collaborative_recommender=self.cf_recommender,
                            alpha=0.5
                        )
                    else:
                        logging.warning(
                            "User-item matrix is empty. Collaborative filtering will not be available.")
                        self.cf_recommender = None
                        self.hybrid_recommender = None
                else:
                    logging.warning("No interactions found in the database.")
                    self.cf_recommender = None
                    self.hybrid_recommender = None

                # Mark data as loaded
                self.data_loaded = True

                # Print loaded tools
                tool_names = [tool.name for tool in self.tools]
                logging.info(f"Loaded tools: {tool_names}")

            except Exception as e:
                raise RuntimeError(f"Failed to initialize CLI: {e}")

    def handle_recommend_similar_tools(self, user_id):
        """
        Handles recommending similar tools based on a tool name provided by the user.
        """
        tool_name = input("Enter the name of a tool you like: ").strip()
        recommendations = self.recommender.recommend_similar_tools(tool_name)

        if recommendations:
            print("\nRecommendations:")
            for tool in recommendations:
                print(
                    f"- {tool.name} (ID: {tool.tool_id}): {tool.description} (Cost: {tool.cost})")
        else:
            print("No similar tools found.")

    def handle_recommend_category_tools(self, user_id):
        """
        Handles recommending tools within a specified category.
        """
        category = input(
            "Enter the category of tools you're interested in: ").strip()
        recommendations = [
            tool for tool in self.tools if tool.category.lower() == category.lower()]

        if recommendations:
            print("\nRecommendations:")
            for tool in recommendations:
                print(
                    f"- {tool.name} (ID: {tool.tool_id}): {tool.description} (Cost: {tool.cost})")
        else:
            print("No tools found in this category.")

    def handle_search_tools(self, user_id):
        """
        Handles searching for tools based on a keyword.
        """
        keyword = input(
            "Enter a keyword to search for tools: ").strip().lower()
        recommendations = [
            tool for tool in self.tools if keyword in tool.name.lower() or keyword in tool.description.lower()
        ]

        if recommendations:
            print("\nSearch Results:")
            for tool in recommendations:
                print(
                    f"- {tool.name} (ID: {tool.tool_id}): {tool.description} (Cost: {tool.cost})")
        else:
            print("No tools found for the given keyword.")

    def handle_rate_tool(self, user_id):
        """
        Handles rating a tool recommended to the user.
        """
        tool_id = int(input("Enter the tool ID you want to rate: ").strip())
        rating = int(input("Enter your rating for the tool (0-5): ").strip())

        if 0 <= rating <= 5:
            self._log_interaction(
                user_id=user_id, tool_id=tool_id, rating=rating)
            print("Thank you for your rating!")
        else:
            print("Invalid rating. Please enter a number between 0 and 5.")

    def start(self):
        """
        Starts the interactive CLI session.
        """
        user_id = self._get_or_create_user()
        self._load_data_and_initialize_recommenders()

        while True:
            print("\n--- LabMateAI Tool Recommender ---")
            print("Please select an option:")
            print("1. Recommend similar tools")
            print("2. Recommend tools within a category")
            print("3. Search tools by keyword")
            print("4. Rate a recommended tool")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ").strip()

            if choice == '1':
                self.handle_recommend_similar_tools(user_id)
            elif choice == '2':
                self.handle_recommend_category_tools(user_id)
            elif choice == '3':
                self.handle_search_tools(user_id)
            elif choice == '4':
                self.handle_rate_tool(user_id)
            elif choice == '5':
                print("Exiting LabMateAI. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")


def main():
    cli = CLI()
    cli.start()
