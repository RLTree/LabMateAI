"""
vertex.py

This module contains the Vertex class used to represent nodes in a graph for LabMate.

The Vertex class enables the creation of graph nodes with edges connecting them to other vertices,
facilitating the construction of a graph that can be used for various graph traversal algorithms.
"""


class Vertex:
    """
    A class to represent a vertex (node) in a graph.

    Attributes
    ----------
    value : any
        The value or identifier for the vertex (e.g., tool name).
    edges : dict
        A dictionary of connected vertices and the weights of the edges.
    """

    def __init__(self, value, cost=0, field=None):
        """
        Initializes a Vertex with a value and an empty dictionary for edges.

        Parameters
        ----------
        value : any
            The value or identifier for the vertex.
        """
        self.value = value
        self.cost = cost
        self.field = field
        self.edges = {}

    def add_edge(self, vertex, weight=0):
        """
        Adds an edge from this vertex to another vertex with an optional weight.

        Parameters
        ----------
        vertex : Vertex
            The vertex to which this vertex is connected.
        weight : int, optional
            The weight of the edge (default is 0).
        """
        self.edges[vertex] = weight

    def get_edges(self):
        """
        Returns a list of vertices that this vertex is connected to.

        Returns
        -------
        list
            A list of connected vertices (neighbors).
        """
        return list(self.edges.keys())
