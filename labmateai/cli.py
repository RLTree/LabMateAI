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

    def __init__(self, recommender=None, cf_recommender=None, tools=None):
        """
        Initializes the CLI by loading data and setting up recommenders.
        """
        try:
            if not recommender or not cf_recommender or not tools:
                # Load data only if recommenders and tools are not provided
                users, tools_df, interactions = load_data()
                user_item_matrix = build_user_item_matrix(interactions)

                # Convert tools_df to a list of Tool objects
                tools = [
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
                recommender = Recommender(tools=tools)

                # Initialize Collaborative Filtering Recommender
                cf_recommender = CollaborativeRecommender(
                    user_item_matrix=user_item_matrix,
                    tools_df=tools_df,
                    n_neighbors=5
                )

            # Assign attributes
            self.tools = tools
            self.recommender = recommender
            self.cf_recommender = cf_recommender

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
                self.handle_recommend_similar_tools()
            elif choice == '2':
                self.handle_recommend_category_tools()
            elif choice == '3':
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
        try:
            recommendations = self.recommender.recommend_similar_tools(
                tool_name=tool_name, num_recommendations=5)
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
        try:
            recommendations = self.recommender.recommend_tools_in_category(
                category_name=category_name)
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
        recommendations = self.recommender.search_and_recommend(
            keyword=keyword)
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
