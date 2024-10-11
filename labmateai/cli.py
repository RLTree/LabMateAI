# cli.py

"""
CLI module for LabMateAI.

This module provides the CLI class, which handles user interactions
and provides tool recommendations based on user input.
"""

import sys
import sqlite3
import pandas as pd
from datetime import datetime
from labmateai.recommender import Recommender, build_user_item_matrix
from labmateai.collaborative_recommender import CollaborativeRecommender
from labmateai.hybrid_recommender import HybridRecommender
from labmateai.tool import Tool


class CLI:
    """
    Command-Line Interface for LabMateAI.
    """

    def __init__(self, db_path='labmate.db'):
        """
        Initializes the CLI, but defers loading data and initializing recommenders.

        Args:
            db_path (str): Path to the SQLite database.
        """
        self.db_path = db_path
        self.tools = None
        self.recommender = None
        self.cf_recommender = None
        self.hybrid_recommender = None
        self.data_loaded = False

    def _get_or_create_user(self):
        """
        Handles user login or sign-up.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        print("\n--- LabMateAI User Login/Signup ---")
        email = input("Enter your email: ").strip().lower()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
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
            VALUES (?, ?, ?, ?)
            """, (user_name, email, department, role))
            conn.commit()
            user_id = cursor.lastrowid
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
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get the next interaction_id
        cursor.execute("SELECT MAX(interaction_id) FROM interactions")
        result = cursor.fetchone()
        next_interaction_id = result[0] + 1 if result[0] else 1249776

        timestamp = datetime.now().isoformat()

        cursor.execute("""
        INSERT INTO interactions (interaction_id, user_id, tool_id, rating, usage_frequency, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (next_interaction_id, user_id, tool_id, rating, usage_frequency, timestamp))
        conn.commit()
        conn.close()

    def _load_data_and_initialize_recommenders(self):
        """
        Loads data and initializes the recommenders.
        """
        if not self.data_loaded:
            try:
                # Connect to the database
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                # Load tools from the tools table
                cursor.execute("SELECT * FROM tools")
                tools_data = cursor.fetchall()
                self.tools = [
                    Tool(
                        tool_id=row[0],
                        name=row[1],
                        category=row[2],
                        features=[feature.strip().lower()
                                  for feature in row[3].split(';') if feature.strip()],
                        cost=row[4],
                        description=row[5],
                        language=row[6],
                        platform=row[7]
                    )
                    for row in tools_data
                ]

                # Initialize the Recommender for content-based recommendations
                self.recommender = Recommender(tools=self.tools)

                # Load user-item interactions from the database
                cursor.execute(
                    "SELECT user_id, tool_id, rating FROM interactions WHERE rating IS NOT NULL")
                interactions_data = cursor.fetchall()
                interactions = pd.DataFrame(interactions_data, columns=[
                                            'user_id', 'tool_id', 'rating'])
                user_item_matrix = build_user_item_matrix(interactions)

                # Initialize Collaborative Filtering Recommender
                self.cf_recommender = CollaborativeRecommender(
                    user_item_matrix=user_item_matrix,
                    tools_df=pd.DataFrame(tools_data, columns=[
                                          'tool_id', 'name', 'category', 'features', 'cost', 'description', 'language', 'platform']),
                    n_neighbors=5
                )

                # Initialize Hybrid Recommender
                self.hybrid_recommender = HybridRecommender(
                    content_recommender=self.recommender,
                    collaborative_recommender=self.cf_recommender,
                    alpha=0.5
                )

                # Mark data as loaded
                self.data_loaded = True

                # Print loaded tools
                tool_names = [tool.name for tool in self.tools]
                print(f"Loaded tools: {tool_names}")

            except Exception as e:
                raise RuntimeError(f"Failed to initialize CLI: {e}")

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

    def handle_recommend_similar_tools(self, user_id):
        """
        Handles the recommendation of similar tools based on a tool name.
        """
        tool_name = input("Enter the name of the tool you like: ").strip()
        num_recommendations = input(
            "Enter the number of recommendations you want: ").strip()

        try:
            num_recommendations = int(num_recommendations)
            if num_recommendations <= 0:
                raise ValueError(
                    "Number of recommendations must be greater than zero.")
        except ValueError as ve:
            print(f"Invalid input for the number of recommendations: {ve}")
            return

        try:
            recommendations = self.recommender.recommend_similar_tools(
                tool_name=tool_name, num_recommendations=num_recommendations)
            if not recommendations:
                print(f"Tool '{tool_name}' not found.")
                return

            print("\nRecommendations:")
            for tool in recommendations:
                print(
                    f"- {tool.name} (ID: {tool.tool_id}): {tool.description} (Cost: {tool.cost})")
                self._log_interaction(user_id, tool.tool_id)

        except ValueError as ve:
            print(ve)

    def handle_recommend_category_tools(self, user_id):
        """
        Handles the recommendation of tools within a specified category.
        """
        category_name = input("Enter the category name: ").strip()
        num_recommendations = input(
            "Enter the number of recommendations you want: ").strip()

        try:
            num_recommendations = int(num_recommendations)
            if num_recommendations <= 0:
                raise ValueError(
                    "Number of recommendations must be greater than zero.")
        except ValueError as ve:
            print(f"Invalid input for the number of recommendations: {ve}")
            return

        try:
            recommendations = self.recommender.recommend_tools_in_category(
                category_name=category_name, num_recommendations=num_recommendations)
            if not recommendations:
                print(f"No tools found for category '{category_name}'.")
                return

            print("\nRecommendations:")
            for tool in recommendations:
                print(
                    f"- {tool.name} (ID: {tool.tool_id}): {tool.description} (Cost: {tool.cost})")
                self._log_interaction(user_id, tool.tool_id)

        except ValueError as ve:
            print(ve)

    def handle_search_tools(self, user_id):
        """
        Handles the search and recommendation of tools based on a keyword.
        """
        keyword = input("Enter a keyword to search for tools: ").strip()
        num_recommendations = input(
            "Enter the number of recommendations you want: ").strip()

        try:
            num_recommendations = int(num_recommendations)
            if num_recommendations <= 0:
                raise ValueError(
                    "Number of recommendations must be greater than zero.")
        except ValueError as ve:
            print(f"Invalid input for the number of recommendations: {ve}")
            return

        recommendations = self.recommender.search_and_recommend(
            keyword=keyword, num_recommendations=num_recommendations)
        if not recommendations:
            print(f"No tools found matching keyword '{keyword}'.")
            return

        print("\nRecommendations:")
        for tool in recommendations:
            print(
                f"- {tool.name} (ID: {tool.tool_id}): {tool.description} (Cost: {tool.cost})")
            self._log_interaction(user_id, tool.tool_id)

    def handle_rate_tool(self, user_id):
        """
        Handles the rating of a recommended tool by the user.
        """
        tool_id = input("Enter the tool ID to rate: ").strip()
        rating = input("Enter your rating for the tool (0-5): ").strip()

        try:
            tool_id = int(tool_id)
            rating = int(rating)
            if rating < 0 or rating > 5:
                raise ValueError("Rating must be between 0 and 5.")
        except ValueError as ve:
            print(f"Invalid input: {ve}")
            return

        self._log_interaction(user_id, tool_id, rating=rating)
        print("Thank you for your feedback!")


def main():
    """
    Main function to run the CLI.
    """
    cli = CLI()
    cli.start()


if __name__ == "__main__":
    main()
