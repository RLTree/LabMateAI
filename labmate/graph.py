"""
graph.py

This module provides the Graph class, which implements a graph data structure
to model relationships between tools. It supports both directed and undirected graphs
and includes methods for adding tools, finding neighbors, performing graph traversal
with Dijkstra's algorithm, and finding the most relevant tools based on specific criteria.

Classes:
    Graph: A class representing a graph of tools, supporting various graph operations.
"""

from math import inf
from heapq import heappush, heappop
from tool import Tool


class Graph:
    """
    Represent a graph where nodes are tools and edges connect similar tools in the graph.
    Supports directed and undirected graphs.

    Attributes:
        graph_dict (dict): Edges are keys and tools are values.
        directed (bool): A flag indicating whether the graph is directed or undirected.
    """

    def __init__(self):
        """
        Initialize the graph.

        Args:
            directed (bool): If True, the graph is directed. Defaults to False.
        """
        self.graph_dict = {}

    def add_node(self, tool):
        """
        Add a tool (node) to the graph.

        Args:
            tool (Vertex): The tool to be added to the graph.
        """
        if isinstance(tool, Tool):
            if tool not in self.graph_dict:
                self.graph_dict[tool] = []

    def add_edge(self, tool1, tool2, weight=0):
        """
        Add an edge (connection) between two tools in the graph.

        Args:
            from_tool (Vertex): The tool from which the edge originates.
            to_tool (Vertex): The tool to which the edge points.
            weight (float): The weight of the edge. Defaults to 0.
        """
        self.graph_dict[tool1].append((tool2, weight))
        self.graph_dict[tool2].append((tool1, weight))

    def get_neighbors(self, tool):
        """
        Get the neighbors of a given tool.

        Args:
            tool (Vertex): The tool for which to find neighbors.

        Returns:
            list: A list of neighboring tools.
        """
        return self.graph_dict.get(tool, [])

    def calculate_simularity(self, tool1, tool2):
        """
        Calculate the similarity between two tools based on their attributes."""
        similarity_score = 0
        CATEGORY_WEIGHT = 1.0
        FEATURE_WEIGHT = 0.5
        COST_WEIGHT = 0.2

        if tool1.category == tool2.category:
            similarity_score += CATEGORY_WEIGHT

        shared_features = set(tool1.features).intersection(set(tool2.features))
        total_features = set(tool1.features).union(set(tool2.features))
        if total_features:
            feature_similarity = len(shared_features) / len(total_features)
            similarity_score += feature_similarity * FEATURE_WEIGHT

        if tool1.cost == tool2.cost:
            similarity_score += COST_WEIGHT

        return similarity_score

    def build_graph(self, tools):
        """
        Build the graph from a list of tools.

        Args:
            tools (list): A list of Tool instances to be added to the graph.
        """
        for tool in tools:
            self.add_node(tool)

        for i, tool1 in enumerate(tools):
            for tool2 in tools[i + 1:]:
                similarity = self.calculate_simularity(tool1, tool2)
                if similarity > 0:
                    self.add_edge(tool1, tool2, similarity)

    def dijkstra(self, start_tool):
        """
        Implement Dijkstra's algorithm to find the shortest path from start tool to all other tools.

        Args:
            start_tool (str): The value of the starting tool (node) for the algorithm.

        Returns:
            dict: A dictionary containing the shortest distances from start tool to each other tool.
        """
        distances = {}
        for tool in self.graph_dict:
            distances[tool] = inf
        distances[start_tool] = 0
        tools_to_explore = [(0, start_tool)]
        while tools_to_explore:
            current_distance, current_tool = heappop(tools_to_explore)
            for neighbor, similarity in self.get_neighbors(current_tool):
                new_distance = current_distance + similarity
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heappush(tools_to_explore, (new_distance, neighbor))
        return distances

    def find_most_relevant_tools(self, start_tool, num_recommendations=5):
        """
        Find the most relevant tools based on the specified criteria using graph traversal.

        Args:
            start_tool (str): The value of the starting tool for the search.
            criteria (dict): A dictionary of criteria to match against tools.
                             Example: {'cost': 'free', 'field': 'genomics', 'feature': 'RNA-seq'}

        Returns:
            list: A list of the most relevant tools that match the criteria.
        """
        distances = self.dijkstra(start_tool)
        relevant_tools = sorted(distances.items(), key=lambda x: x[1])
        return [tool for tool, distance in relevant_tools[:num_recommendations]]

    def __repr__(self):
        """
        Return a string representation of the graph.

        Returns:
            str: A string representing the graph, showing each tool (node)
                 and its connected neighbors with the respective weights.
        """
        graph_repr = ""
        for tool_value, tool in self.graph_dict.items():
            neighbor_str = ", ".join(
                [f"{neighbor} (weight: {weight})" for neighbor, weight in tool.get_edges()])
            graph_repr += f"{tool_value}: [{neighbor_str}]\n"
        return graph_repr
