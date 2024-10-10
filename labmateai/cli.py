# cli.py

"""
CLI module for LabMateAI.

This module provides the CLI class, which handles user interactions
and provides tool recommendations based on user input.
"""

import sys
from unittest.mock import patch
from labmateai.recommender import Recommender, load_data, build_user_item_matrix
from labmateai.collaborative_recommender import CollaborativeRecommender
from labmateai.tool import Tool


class CLI:
    """
    Command-Line Interface for LabMateAI.
    """

    def __init__(self):
        """
        Initializes the CLI, but defers loading data and initializing recommenders.
        """
        self.tools = None
        self.recommender = None
        self.cf_recommender = None
        self.data_loaded = False

    def _load_data_and_initialize_recommenders(self):
        """
        Loads data and initializes the recommenders.
        """
        if not self.data_loaded:
            try:
                # Load data
                users, tools_df, interactions = load_data()
                user_item_matrix = build_user_item_matrix(interactions)

                # Convert tools_df to a list of Tool objects
                self.tools = [
                    Tool(
                        tool_id=int(row['tool_id']),
                        name=row['name'],  # Fixed from 'tool_name' to 'name'
                        category=row['category'],
                        features=[feature.strip().lower()
                                  for feature in row['features'].split(';') if feature.strip()],
                        cost=row['cost'],
                        description=row['description'],
                        url=row['url'],
                        language=row['language'],
                        platform=row['platform']
                    )
                    for index, row in tools_df.iterrows()
                ]

                # Initialize the Recommender for content-based recommendations
                self.recommender = Recommender(tools=self.tools)

                # Initialize Collaborative Filtering Recommender
                self.cf_recommender = CollaborativeRecommender(
                    user_item_matrix=user_item_matrix,
                    tools_df=tools_df,
                    n_neighbors=5
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
        while True:
            print("\n--- LabMateAI Tool Recommender ---")
            print("Please select an option:")
            print("1. Recommend similar tools")
            print("2. Recommend tools within a category")
            print("3. Search tools by keyword")
            print("4. Exit")

            choice = input("Enter your choice (1-4): ").strip()

            if choice == '1':
                self._load_data_and_initialize_recommenders()
                self.handle_recommend_similar_tools()
            elif choice == '2':
                self._load_data_and_initialize_recommenders()
                self.handle_recommend_category_tools()
            elif choice == '3':
                self._load_data_and_initialize_recommenders()
                self.handle_search_tools()
            elif choice == '4':
                print("Exiting LabMateAI. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

    def handle_recommend_similar_tools(self):
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
            print("\nRecommendations:")
            for tool in recommendations:
                print(
                    f"- {tool.name} (ID: {tool.tool_id}): {tool.description} (Cost: {tool.cost})")
        except ValueError as ve:
            print(ve)

    def handle_recommend_category_tools(self):
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
            print("\nRecommendations:")
            for tool in recommendations:
                print(
                    f"- {tool.name} (ID: {tool.tool_id}): {tool.description} (Cost: {tool.cost})")
        except ValueError as ve:
            print(ve)

    def handle_search_tools(self):
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
        if recommendations:
            print("\nRecommendations:")
            for tool in recommendations:
                print(
                    f"- {tool.name} (ID: {tool.tool_id}): {tool.description} (Cost: {tool.cost})")
        else:
            print(f"No tools found matching keyword '{keyword}'.")


def main():
    """
    Main function to run the CLI.
    """
    cli = CLI()
    cli.start()


if __name__ == "__main__":
    main()
