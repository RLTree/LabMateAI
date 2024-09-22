"""
Recommender module for suggesting tools based on user input.
"""

from graph import Graph
from tree import ToolTree


class Recommender:
    """
    A class that integrates the graph and tree structures to recommend tools based input.
    """

    def __init__(self, tools):
        """
        Initializes the recommender with a list of tools.

        Args:
            tools (list): A list of tools to be used for recommendations.
        """

        self.graph = Graph()
        self.tree = ToolTree()
        self.tools = tools

        print(f"Loaded tools: {self.tools}")

    def build_recommendation_system(self):
        """
        Builds the recommendation system by constructing the graph and tree.
        """

        self.graph.build_graph(self.tools)
        self.tree.build_tree(self.tools)

    def recommend_similar_tools(self, tool_name, num_recommendations=5):
        """
        Recommends similar tools based on the input tool name.

        Args:
            tool_name (str): The name of the tool to find recommendations for.
            num_recommendations (int): The number of recommendations to return.

        Returns:
            list: A list of recommended tools.
        """

        # Retrieve recommendations (tool names) from the graph
        recommended_tool_names = self.graph.find_most_relevant_tools(
            tool_name, num_recommendations)

        # Debugging: Print the recommended tool names to see if they are retrieved
        print(f"Recommended tools for {tool_name}: {recommended_tool_names}")

        # Look up full tool details for each recommended tool name
        recommendations = [
            tool for tool in self.tools if tool.name in recommended_tool_names]

        # Debugging: Print the full tool information retrieved
        print(f"Full tool details: {recommendations}")

        return recommendations

    def recommend_tools_in_category(self, category_name):
        """
        Recommends tools based on the specified category.

        Args:
            category_name (str): The name of the category to find recommendations for.

        Returns:
            list: A list of recommended tools in the specified category.
        """
        recommendations = self.tree.get_tools_in_category(category_name)
        return recommendations

    def search_and_recommend(self, keyword):
        """
        Searches for tools based on a keyword and recommends them.

        Args:
            keyword (str): The keyword to search for.

        Returns:
            list: A list of recommended tools based on the search.
        """

        recommendations = self.tree.search_tools(keyword)
        return recommendations

    def recommend(self, tool_name=None, category_name=None, keyword=None, num_recommendations=5):
        """
        Provides recommendations based on the input parameters.

        Args:
            tool_name (str): The name of the tool to find recommendations for.
            category_name (str): The name of the category to find recommendations for.
            keyword (str): The keyword to search for.

        Returns:
            list: A list of recommended tools based on the input parameters.
        """

        if tool_name:
            recommendations = self.recommend_similar_tools(
                tool_name, num_recommendations)
        elif category_name:
            recommendations = self.recommend_tools_in_category(category_name)
        elif keyword:
            recommendations = self.search_and_recommend(keyword)
        else:
            return []
        return recommendations

    def display_recommendations(self, recommendations):
        """
        Displays the recommended tools.

        Args:
            recommendations (list): A list of recommended tools to display.
        """
        if not recommendations:
            print("No recommendations found.")
        else:
            for tool in recommendations:
                print(
                    f"{tool.name} - {tool.description} (Category: {tool.category}, Cost: {tool.cost})"
                )
