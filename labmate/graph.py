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
from .vertex import Vertex


class Graph:
    """
    Represent a graph where nodes are tools and edges connect similar tools in the graph.
    Supports directed and undirected graphs.

    Attributes:
        graph_dict (dict): Edges are keys and tools are values.
        directed (bool): A flag indicating whether the graph is directed or undirected.
    """

    def __init__(self, directed=False):
        """
        Initialize the graph.

        Args:
            directed (bool): If True, the graph is directed. Defaults to False.
        """
        self.graph_dict = {}
        self.directed = directed

    def add_tool(self, tool):
        """
        Add a tool (node) to the graph.

        Args:
            tool (Vertex): The tool to be added to the graph.
        """
        if isinstance(tool, Vertex):
            self.graph_dict[tool.value] = tool
        else:
            raise TypeError("Expected a Vertex instance.")

    def add_neighbor(self, from_tool, to_tool, weight=0):
        """
        Add a neighbor (edge) between two tools in the graph.

        Args:
            from_tool (Vertex): The tool from which the edge originates.
            to_tool (Vertex): The tool to which the edge points.
            weight (float): The weight of the edge. Defaults to 0.
        """
        self.graph_dict[from_tool.value].add_edge(to_tool.value, weight)
        if not self.directed:
            self.graph_dict[to_tool.value].add_edge(from_tool.value, weight)

    def get_neighbors(self, tool):
        """
        Get all neighboring tools connected to the specified tool.

        Args:
            tool (Vertex): The tool whose neighbors are to be retrieved.

        Returns:
            list: A list of neighboring tools.
        """
        neighbor_tools = []
        for i in self.graph_dict[tool.value].get_edges():
            neighbor_tools += i
        return neighbor_tools

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
            for neighbor, edge_weight in self.graph_dict[current_tool].get_edges():
                new_distance = current_distance + edge_weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heappush(tools_to_explore, (new_distance, neighbor))
        return distances

    def find_most_relevant_tools(self, start_tool, criteria):
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
        relevant_tools = []
        for distance in distances:
            if self.matches_criteria(distance, criteria):
                relevant_tools.append(distance)
        relevant_tools.sort(lambda x: x[1])
        return [tool for tool, distance in relevant_tools]

    def matches_criteria(self, tool, criteria):
        """
        Check if the tool matches the given criteria.

        Args:
            tool (Vertex): The tool to be checked.
            criteria (dict): A dictionary of criteria to match against the tool.
                             Example: {'cost': 'free', 'field': 'genomics', 'feature': 'RNA-seq'}

        Returns:
            bool: True if the tool matches the criteria, False otherwise.
        """
        if 'cost' in criteria and criteria['cost'] < tool.cost:
            return False
        if 'field' in criteria and criteria['field'] != tool.field:
            return False
        if 'feature' in criteria and criteria['feature'] not in tool.features:
            return False
        return True

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
