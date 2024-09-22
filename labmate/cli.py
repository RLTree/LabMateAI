"""
CLI module for the LabMate recommendation system.

This module provides a command-line interface to interact with the LabMate recommendation system.

Usage:

    -t, --tool TOOL_NAME       Recommend tools similar to the given tool.
    -c, --category CATEGORY    Recommend tools from the specified category.
    -s, --search KEYWORD       Search for tools using a keyword.
    -n, --num NUM_RECOMMENDATIONS  Specify the number of recommendations to display.

Examples:
    python cli.py -t 'Microscope' -n 3
    python cli.py -c 'Biology'
    python cli.py -s 'Laser'
"""

import argparse
from recommender import Recommender
from data_loader import load_tools_from_json
import sys


class CLI:
    """
    Command-line interface for interacting with the LabMate recommendation system.
    """

    def __init__(self, tools):
        """
        Initializes the CLI with a Recommender instance and available tools.
        """
        self.recommender = Recommender(tools)

    def start(self):
        """
        Start the CLI and begin accepting user input.
        """
        parser = argparse.ArgumentParser(
            description="LabMate: A Scientific Tool Recommendation System")

        parser.add_argument('-t', '--tool', type=str,
                            help="Recommend tools similar to the given tool name.")
        parser.add_argument('-c', '--category', type=str,
                            help="Recommend tools from the specified category.")
        parser.add_argument('-s', '--search', type=str,
                            help="Search for tools based on a keyword.")
        parser.add_argument('-n', '--num', type=int, default=5,
                            help="Number of recommendations to display.")

        # Parse the arguments from the command line
        args = parser.parse_args()

        # Check if any arguments were provided. If not, trigger interactive mode.
        if len(sys.argv) == 1:
            print("No arguments provided. Switching to interactive mode.")
            self.interactive_prompt()
        else:
            self.handle_recommendation(args)

    def interactive_prompt(self):
        """
        Interactive prompt for user input when no command-line arguments are provided.
        """
        print("Welcome to LabMate! Please select an option:")
        print("1: Recommend tools similar to a specific tool")
        print("2: Recommend tools from a category")
        print("3: Search tools by a keyword")
        print("4: Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            tool_name = input("Enter the tool name: ")
            num_recommendations = input(
                "Enter the number of recommendations: ")
            recommendations = self.recommender.recommend_similar_tools(
                tool_name=tool_name, num_recommendations=int(num_recommendations))
        elif choice == '2':
            category_name = input("Enter the category name: ")
            recommendations = self.recommender.recommend_tools_in_category(
                category_name)
        elif choice == '3':
            keyword = input("Enter a keyword: ")
            recommendations = self.recommender.search_and_recommend(keyword)
        elif choice == '4':
            print("Exiting LabMate. Goodbye!")
            return
        else:
            print("Invalid choice. Please try again.")
            return self.interactive_prompt()

        # Display the recommendations if available
        if recommendations:
            self.recommender.display_recommendations(recommendations)
        else:
            print("No recommendations found for the given input.")

    def handle_recommendation(self, args):
        """
        Handle the recommendation based on user input.
        """
        recommendations = []

        if args.tool:
            recommendations = self.recommender.recommend_similar_tools(
                tool_name=args.tool, num_recommendations=args.num)
        elif args.category:
            recommendations = self.recommender.recommend_tools_in_category(
                category_name=args.category)
        elif args.search:
            recommendations = self.recommender.search_and_recommend(
                keyword=args.search)
        else:
            print("Please provide a valid input. Use -h or --help for more information.")
            return

        # Display the recommendations if available
        if recommendations:
            self.recommender.display_recommendations(recommendations)
        else:
            print("No recommendations found for the given input.")


def main():
    """
    Main entry point for running the CLI.
    """
    tools = load_tools_from_json('../data/tools.json')

    # Initialize and start the CLI
    cli = CLI(tools)
    cli.start()


if __name__ == "__main__":
    main()
