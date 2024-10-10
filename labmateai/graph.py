# graph.py

"""
This module provides the Graph class, which implements a graph data structure
to model relationships between tools. It supports both directed and undirected graphs
and includes methods for adding tools, finding neighbors, performing graph traversal
with Dijkstra's algorithm, and finding the most relevant tools based on specific criteria.

Classes:
    Graph: A class representing a graph of tools, supporting various graph operations.
"""

import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .tool import Tool


class Graph:
    """
    Represent a graph where nodes are tools and edges connect similar tools in the graph.
    Supports directed and undirected graphs.
    """

    def __init__(self, tools):
        """
        Initialize the graph.
        """
        self.tools = tools
        self.graph = nx.Graph()
        if tools:  # Only build the graph if tools are provided
            self.build_graph(tools)

    def add_node(self, tool):
        """
        Add a tool (node) to the graph.

        Args:
            tool (Tool): The tool to add.
        """
        if isinstance(tool, Tool):
            if tool not in self.graph:
                self.graph.add_node(tool)

    def add_edge(self, tool1, tool2, similarity=0.0):
        """
        Add an edge (connection) between two tools in the graph.

        Args:
            tool1 (Tool): The first tool.
            tool2 (Tool): The second tool.
            similarity (float): The similarity score between the tools.
        """
        if not self.graph.has_edge(tool1, tool2):
            self.graph.add_edge(tool1, tool2, weight=similarity)

    def build_graph(self, tools):
        """
        Build the graph from a list of tools using TF-IDF and cosine similarity.

        Args:
            tools (list): A list of Tool instances to be added to the graph.
        """
        # Add all tools as nodes
        for tool in tools:
            self.add_node(tool)

        # Add edges based on similarity threshold
        SIMILARITY_THRESHOLD = 0.2  # Adjust as needed

        for i, tool1 in enumerate(tools):
            for j, tool2 in enumerate(tools):
                if i >= j:
                    continue  # Avoid duplicate edges and self-loops
                similarity = self.calculate_similarity(
                    tool1, tool2)
                if round(similarity, 2) >= SIMILARITY_THRESHOLD:
                    self.add_edge(tool1, tool2, similarity)
                # Debugging: Uncomment to print similarity values
                # print(f"Similarity between {tool1.name} and {tool2.name}: {similarity:.2f}")

    def calculate_similarity(self, tool1, tool2):
        """
        Calculate the similarity between two tools based on their features using TF-IDF and cosine similarity.

        Args:
            tool1 (Tool): The first tool.
            tool2 (Tool): The second tool.

        Returns:
            float: The similarity score between the tools.
        """
        # Feature Similarity
        vectorizer = TfidfVectorizer(stop_words='english')
        feature_strings = [" ".join(tool1.features), " ".join(tool2.features)]
        tfidf_matrix = vectorizer.fit_transform(feature_strings)

        feature_similarity = cosine_similarity(tfidf_matrix)[0, 1]

        # Category Similarity
        category_similarity = 1.5 if tool1.category == tool2.category else 0.0

        # Cost similarity
        cost_similarity = 0.5 if tool1.cost == tool2.cost else 0.0

        # Language similarity
        language_similarity = 0.3 if tool1.language == tool2.language else 0.0

        # Platform similarity (check if there is any overlap in platforms)
        platform_overlap = set(tool1.platform.split(
            ", ")) & set(tool2.platform.split(", "))
        platform_similarity = 0.2 if platform_overlap else 0.0

        # Weighted Sum of Similarities
        total_similarity = (
            2.0 * feature_similarity +
            1.5 * category_similarity +
            0.5 * cost_similarity +
            0.3 * language_similarity +
            0.2 * platform_similarity
        )

        # Normalize the similarity score
        max_similarity = 2.0 + 1.5 + 0.5 + 0.3 + 0.2
        normalized_similarity = total_similarity / max_similarity

        return normalized_similarity

    def find_most_relevant_tools(self, start_tool, num_recommendations=5):
        """
        Find the most relevant tools based on similarity scores.

        Args:
            start_tool (Tool): The starting tool for the search.
            num_recommendations (int): The number of recommendations to return.

        Returns:
            list: A list of the most relevant Tool objects.
        """
        if start_tool not in self.graph:
            raise ValueError(
                f"Start tool '{start_tool.name}' not found in the graph.")

        # Get neighbors sorted by similarity (descending order)
        neighbors = sorted(self.graph[start_tool].items(
        ), key=lambda x: x[1]['weight'], reverse=True)
        recommended_tools = [neighbor for neighbor,
                             attrs in neighbors[:num_recommendations]]
        return recommended_tools

    def __repr__(self):
        """
        Return a string representation of the graph.

        Returns:
            str: A string representing the graph, showing each tool (node)
                 and its connected neighbors with the respective weights.
        """
        graph_repr = ""
        for tool in self.graph.nodes:
            neighbors = self.graph[tool]
            neighbor_str = ", ".join(
                [f"{neighbor.name} (similarity: {attrs['weight']:.2f})" for neighbor, attrs in neighbors.items()])
            graph_repr += f"{tool.name}: [{neighbor_str}]\n"
        return graph_repr
