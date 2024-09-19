"""
CLI module for the LabMate recommendation system.

This module provides a command-line interface to interact with the LabMate recommendation system.

Usage:

    -t, --tool TOOL_NAME       Recommend tools similar to the given tool.
    -c, --category CATEGORY    Recommend tools from the specified category.
    -s, --search KEYWORD       Search for tools using a keyword.
    -n, --num NUM_RECOMMENDATIONS  Specify the number of recommendations to display.
    -H, --help                 Display this help message.

Examples:
    python cli.py -t 'Microscope' -n 3
    python cli.py -c 'Biology'
    python cli.py -s 'Laser'
"""

import argparse
from .recommender import Recommender
from .data_loader import load_tools_from_json


class CLI:
    """
    Command-line interface for interacting with the LabMate recommendation system.
    """

    def __init__(self, tools):
        """
        Initializes the CLI with a Recommender instance and available tools."""

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
        parser.add_argument('-H', '--help', action='store_true',
                            help="Display help message.")

        args = parser.parse_args()

        if args.help:
            self.display_help()
        else:
            self.handle_recommendation(args)

    def handle_recommendation(self, args):
        """
        Handle the recommendation based on user input.
        """

        if args.tool:
            recommendations = self.recommender.recommend(
                tool_name=args.tool, num_recommendations=args.num)
        elif args.category:
            recommendations = self.recommender.recommend(
                category_name=args.category)
        elif args.search:
            recommendations = self.recommender.recommend(keyword=args.search)
        else:
            print("Please provide a valid input. Use -H or --help for more information.")

        self.recommender.display_recommendations(recommendations)

    def display_help(self):
        """
        Display help information for the CLI.
        """

        print("Usage:")
        print("  -t, --tool TOOL_NAME       Recommend tools similar to the given tool.")
        print("  -c, --category CATEGORY    Recommend tools from the specified category.")
        print("  -s, --search KEYWORD       Search for tools using a keyword.")
        print("  -n, --num NUM_RECOMMENDATIONS  Specify the number of recommendations to display.")
        print("  -H, --help                 Display this help message.")

        print("\nExamples:")
        print("  python cli.py -t 'Microscope' -n 3")
        print("  python cli.py -c 'Biology'")
        print("  python cli.py -s 'Laser'")


def main():
    """
    Main entry point for running the CLI.
    """
    tools = load_tools_from_json('data/tools.json')

    cli = CLI(tools)
    cli.start()
