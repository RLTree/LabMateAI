"""
Unit tests for the Graph class in the labmateai module.
"""

import unittest
from labmateai.graph import Graph
from labmateai.data_loader import load_tools_from_json


class TestGraph(unittest.TestCase):
    """
    Unit tests for the Graph class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize the graph before all tests.
        """
        cls.tools = load_tools_from_json('tools.json')
        cls.graph = Graph()
        cls.graph.build_graph(cls.tools)

    def test_graph_nodes(self):
        """
        Test that all tools are added as nodes.
        """
        self.assertEqual(len(cls.graph.nodes), len(cls.tools))

    def test_graph_edges(self):
        """
        Test that edges are correctly added.
        """
        total_edges = sum(len(edges) for edges in cls.graph.edges.values())
        self.assertTrue(total_edges > 0)

    def test_get_neighbors(self):
        """
        Test retrieving neighbors of a node.
        """
        tool = cls.tools[0]
        neighbors = cls.graph.get_neighbors(tool)
        self.assertIsInstance(neighbors, list)
