# graph.py

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
from itertools import count
from heapq import heappush, heappop
from .tool import Tool


class Graph:
    """
    Represent a graph where nodes are tools and edges connect similar tools in the graph.
    Supports directed and undirected graphs.

    Attributes:
        adj_list (dict): Adjacency list representing the graph. Keys are Tool instances,
                         and values are lists of tuples (neighbor Tool, weight).
    """

    def __init__(self):
        """
        Initialize the graph.
        """
        self.adj_list = {}

    def add_node(self, tool):
        """
        Add a tool (node) to the graph.

        Args:
            tool (Tool): The tool to add.
        """
        if isinstance(tool, Tool):
            if tool not in self.adj_list:
                self.adj_list[tool] = []

    def add_edge(self, tool1, tool2, weight=0):
        """
        Add an edge (connection) between two tools in the graph.

        Args:
            tool1 (Tool): The first tool.
            tool2 (Tool): The second tool.
            weight (float): The weight of the edge.
        """
        if not any(neighbor == tool2 for neighbor, _ in self.adj_list[tool1]):
            self.adj_list[tool1].append((tool2, weight))
        if not any(neighbor == tool1 for neighbor, _ in self.adj_list[tool2]):
            self.adj_list[tool2].append((tool1, weight))

    def remove_edge(self, tool1, tool2):
        """
        Remove an edge between two tools in the graph.

        Args:
            tool1 (Tool): The first tool.
            tool2 (Tool): The second tool.

        Raises:
            ValueError: If the edge does not exist.
        """
        if tool1 in self.adj_list and tool2 in self.adj_list:
            original_length = len(self.adj_list[tool1])
            self.adj_list[tool1] = [
                (neighbor, weight) for neighbor, weight in self.adj_list[tool1] if neighbor != tool2
            ]
            self.adj_list[tool2] = [
                (neighbor, weight) for neighbor, weight in self.adj_list[tool2] if neighbor != tool1
            ]
            if len(self.adj_list[tool1]) == original_length:
                raise ValueError(
                    f"No edge exists between '{tool1.name}' and '{tool2.name}'.")

    def remove_tool(self, tool):
        """
        Remove a tool (node) from the graph, along with all its edges.

        Args:
            tool (Tool): The tool to remove.

        Raises:
            KeyError: If the tool does not exist in the graph.
        """
        if tool not in self.adj_list:
            raise KeyError(f"Tool '{tool.name}' does not exist in the graph.")

        # Remove the tool from all neighbors' adjacency lists
        for neighbor, _ in self.adj_list[tool]:
            self.adj_list[neighbor] = [
                (n, w) for n, w in self.adj_list[neighbor] if n != tool
            ]

        # Remove the tool from the graph
        del self.adj_list[tool]

    def get_neighbors(self, tool):
        """
        Get the neighbors of a given tool.

        Args:
            tool (Tool): The tool whose neighbors are to be retrieved.

        Returns:
            list: A list of tuples (neighbor Tool, weight).
        """
        return self.adj_list.get(tool, [])

    def calculate_simularity(self, tool1, tool2):
        """
        Calculate the similarity between two tools based on their attributes.

        Args:
            tool1 (Tool): The first tool.
            tool2 (Tool): The second tool.

        Returns:
            float: The similarity score.
        """
        similarity_score = 0
        CATEGORY_WEIGHT = 1.0
        FEATURE_WEIGHT = 2.0
        COST_WEIGHT = 0.2

        if tool1.category == tool2.category:
            similarity_score += CATEGORY_WEIGHT

        shared_features = set(tool1.features).intersection(set(tool2.features))
        total_features = set(tool1.features).union(set(tool2.features))
        if total_features:
            feature_similarity = len(shared_features) / len(total_features)
            similarity_score += feature_similarity * FEATURE_WEIGHT

        if tool1.cost.lower() == tool2.cost.lower():
            similarity_score += COST_WEIGHT

        return similarity_score

    def build_graph(self, tools):
        """
        Build the graph from a list of tools.

        Args:
            tools (list): A list of Tool instances to be added to the graph.
        """
        MAX_SIMILARITY_SCORE = 3.2
        SIMILARITY_THRESHOLD = 0.3

        for tool in tools:
            self.add_node(tool)

        for i, tool1 in enumerate(tools):
            for tool2 in tools[i + 1:]:
                similarity = self.calculate_simularity(tool1, tool2)
                if similarity > 0:
                    normalized_similarity = similarity / MAX_SIMILARITY_SCORE
                    if normalized_similarity > SIMILARITY_THRESHOLD:
                        dissimilarity = 1.0 - normalized_similarity
                        self.add_edge(tool1, tool2, dissimilarity)

    def dijkstra(self, start_tool):
        """
        Implement Dijkstra's algorithm to find the shortest path from start tool to all other tools.

        Args:
            start_tool (Tool): The starting tool for the algorithm.

        Returns:
            dict: A dictionary containing the shortest distances from start tool to each other tool.

        Raises:
            ValueError: If the start_tool is not in the graph.
        """
        if start_tool not in self.adj_list:
            raise ValueError(
                f"Start tool '{start_tool.name}' not found in the graph.")

        distances = {tool: inf for tool in self.adj_list}
        distances[start_tool] = 0
        counter = count()
        tools_to_explore = [(0, next(counter), start_tool)]

        while tools_to_explore:
            current_distance, _, current_tool = heappop(tools_to_explore)

            for neighbor, similarity in self.get_neighbors(current_tool):
                new_distance = current_distance + similarity
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heappush(tools_to_explore,
                             (new_distance, next(counter), neighbor))

        return distances

    def find_most_relevant_tools(self, start_tool, num_recommendations=5):
        """
        Find the most relevant tools based on the specified criteria using graph traversal.

        Args:
            start_tool (Tool): The starting tool for the search.
            num_recommendations (int): The number of recommendations to return.

        Returns:
            list: A list of the most relevant tools.

        Raises:
            ValueError: If the start_tool is not in the graph.
        """

        # Check if start_tool exists in the graph
        if start_tool not in self.adj_list:
            raise ValueError(
                f"Start tool '{start_tool.name}' not found in the graph.")

        # Run Dijkstra's algorithm to get the "distances" (dissimilarity scores)
        distances = self.dijkstra(start_tool)

        # Sort tools by their distance (dissimilarity) to the start tool
        relevant_tools = sorted(distances.items(), key=lambda x: x[1])

        # Exclude the starting tool from the recommendations
        filtered_tools = [tool for tool,
                          distance in relevant_tools if tool != start_tool]

        # Return the top recommendations (up to num_recommendations)
        return filtered_tools[:num_recommendations]

    def __repr__(self):
        """
        Return a string representation of the graph.

        Returns:
            str: A string representing the graph, showing each tool (node)
                 and its connected neighbors with the respective weights.
        """
        graph_repr = ""
        for tool, neighbors in self.adj_list.items():
            neighbor_str = ", ".join(
                [f"{neighbor.name} (weight: {weight})" for neighbor,
                 weight in neighbors]
            )
            graph_repr += f"{tool.name}: [{neighbor_str}]\n"
        return graph_repr
