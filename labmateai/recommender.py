"""
Recommender module for suggesting tools based on user input.
"""

from .graph import Graph
from .tree import ToolTree


class Recommender:
    """
    A class that integrates the graph and tree structures to recommend tools based on input.
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
        self.tool_names = {tool.name for tool in tools}
        self.build_recommendation_system()

        # Enhanced print for clarity
        print(f"Loaded tools: {[tool.name for tool in self.tools]}")

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

        if tool_name not in self.tool_names:
            raise ValueError(f"Tool '{tool_name}' not found.")

        selected_tool = next(
            (tool for tool in self.tools if tool.name == tool_name), None)

        if not selected_tool:
            print(f"Tool '{tool_name}' not found.")
            return []

        recommendations = self.graph.find_most_relevant_tools(
            selected_tool, num_recommendations)

        unique_recommendations = []
        seen = set()

        for tool in recommendations:
            if tool.name != tool_name and tool.name not in seen:
                unique_recommendations.append(tool)
                seen.add(tool.name)
            if len(unique_recommendations) >= num_recommendations:
                break

        return unique_recommendations

    def recommend_tools_in_category(self, category_name):
        """
        Recommends tools based on the specified category.

        Args:
            category_name (str): The name of the category to find recommendations for.

        Returns:
            list: A list of recommended tools in the specified category.
        """
        try:
            recommendations = self.tree.get_tools_in_category(category_name)
        except ValueError as e:
            raise ValueError(str(e))
        unique_recommendations = []
        seen = set()
        for tool in recommendations:
            if tool.name not in seen:
                unique_recommendations.append(tool)
                seen.add(tool.name)
        return unique_recommendations

    def search_and_recommend(self, keyword):
        """
        Searches for tools based on a keyword and recommends them.

        Args:
            keyword (str): The keyword to search for.

        Returns:
            list: A list of recommended tools based on the search.
        """

        recommendations = self.tree.search_tools(keyword)

        unique_recommendations = []
        seen = set()

        for tool in recommendations:
            if tool.name not in seen:
                unique_recommendations.append(tool)
                seen.add(tool.name)

        return unique_recommendations

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

        print("\nRecommended Tools:")
        if not recommendations:
            print("No recommendations found.")
        else:
            for tool in recommendations:
                print(
                    f"{tool.name} - {tool.description} (Category: {tool.category}, Cost: {tool.cost})"
                )
