# labmateai/cli.py

import sys
from labmateai.recommender import Recommender
from labmateai.data_loader import load_tools_from_json


class CLI:
    """
    A class to handle the command-line interface for LabMate.
    """

    def __init__(self, recommender):
        """
        Initialize the CLI with a Recommender instance.

        Args:
            recommender (Recommender): An instance of the Recommender class.
        """
        self.recommender = recommender

    def start(self):
        """
        Start the CLI. If command-line arguments are provided, process them.
        Otherwise, enter interactive mode.
        """
        if len(sys.argv) > 1:
            # Handle command-line arguments if needed
            pass
        else:
            print("No arguments provided. Switching to interactive mode.\n")
            self.interactive_mode()

    def interactive_mode(self):
        """
        Handle the interactive mode of the CLI.
        """
        while True:
            print("Please choose an option:")
            print("1. Recommend similar tools")
            print("2. Recommend tools in a category")
            print("3. Search tools by keyword")
            print("4. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                self.handle_recommend_similar_tools()
            elif choice == '2':
                self.handle_recommend_tools_in_category()
            elif choice == '3':
                self.handle_search_tools_by_keyword()
            elif choice == '4':
                print("Exiting LabMate. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.\n")

    def handle_recommend_similar_tools(self):
        """
        Handle the logic for recommending similar tools.
        """
        tool_name = input("Enter the tool name: ").strip()
        try:
            recommendations = self.recommender.recommend_similar_tools(
                tool_name, 5)
            if recommendations:
                print("\nRecommendations:")
                for tool in recommendations:
                    print(f"- {tool.name}: {tool.description}")
                print("")  # Add an empty line for better readability
            else:
                print(f"No recommendations found for tool '{tool_name}'.\n")
        except ValueError as ve:
            print(str(ve) + "\n")

    def handle_recommend_tools_in_category(self):
        """
        Handle the logic for recommending tools in a specific category.
        """
        category_name = input("Enter the category name: ").strip()
        try:
            recommendations = self.recommender.recommend_tools_in_category(
                category_name)
            if recommendations:
                print("\nRecommendations:")
                for tool in recommendations:
                    print(f"- {tool.name}: {tool.description}")
                print("")  # Add an empty line for better readability
            else:
                print(f"No tools found in category '{category_name}'.\n")
        except ValueError as ve:
            print(str(ve) + "\n")

    def handle_search_tools_by_keyword(self):
        """
        Handle the logic for searching tools by a keyword.
        """
        keyword = input("Enter the keyword to search: ").strip()
        recommendations = self.recommender.search_and_recommend(keyword)
        if recommendations:
            print("\nRecommendations:")
            for tool in recommendations:
                print(f"- {tool.name}: {tool.description}")
            print("")  # Add an empty line for better readability
        else:
            print(f"No tools found matching keyword '{keyword}'.\n")


def main():
    """
    The main function for the LabMate CLI.
    """
    # Initialize the Recommender and CLI
    tools = load_tools_from_json()
    recommender = Recommender(tools)
    cli = CLI(recommender)
    cli.start()


if __name__ == "__main__":
    main()
