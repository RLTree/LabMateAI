# labmateai/tests/test_tree.py

"""
Test Suite for Tree Module in LabMateAI.

This test suite ensures that the TreeNode and ToolTree classes function correctly,
covering various scenarios including normal operations, edge cases, and error handling.
"""

import unittest
from unittest.mock import patch
import pandas as pd
from io import StringIO

from labmateai.tree import TreeNode, ToolTree


# Define a simple Tool class for testing purposes
class Tool:
    """
    A mock Tool class for testing the ToolTree.
    """
    def __init__(self, tool_id, name, category, description, features):
        self.tool_id = tool_id
        self.name = name
        self.category = category
        self.description = description
        self.features = features


class TestTreeNode(unittest.TestCase):
    """
    Test cases for the TreeNode class.
    """

    def test_initialization_without_tool(self):
        """
        Test initializing a TreeNode without a tool.
        """
        node = TreeNode(name="Genomics")
        self.assertEqual(node.name, "genomics")
        self.assertEqual(node.original_name, "Genomics")
        self.assertIsNone(node.tool)
        self.assertEqual(node.children, [])

    def test_initialization_with_tool_and_original_name(self):
        """
        Test initializing a TreeNode with a tool and a custom original name.
        """
        tool = Tool(
            tool_id=1,
            name="Alpha",
            category="Genomics",
            description="Alpha Description",
            features=["sequence_analysis", "alignment"]
        )
        node = TreeNode(name="Alpha", tool=tool, original_name="Alpha Original")
        self.assertEqual(node.name, "alpha")
        self.assertEqual(node.original_name, "Alpha Original")
        self.assertEqual(node.tool, tool)
        self.assertEqual(node.children, [])

    def test_add_child(self):
        """
        Test adding a child node to a parent TreeNode.
        """
        parent = TreeNode(name="Genomics")
        child = TreeNode(name="Alpha")
        parent.add_child(child)
        self.assertIn(child, parent.children)
        self.assertEqual(len(parent.children), 1)

    def test_is_leaf_true(self):
        """
        Test that a TreeNode with no children is a leaf.
        """
        node = TreeNode(name="Genomics")
        self.assertTrue(node.is_leaf())

    def test_is_leaf_false(self):
        """
        Test that a TreeNode with children is not a leaf.
        """
        parent = TreeNode(name="Genomics")
        child = TreeNode(name="Alpha")
        parent.add_child(child)
        self.assertFalse(parent.is_leaf())


class TestToolTree(unittest.TestCase):
    """
    Test cases for the ToolTree class.
    """

    def setUp(self):
        """
        Set up a ToolTree instance with sample tools for testing.
        """
        self.tool1 = Tool(
            tool_id=1,
            name="Alpha",
            category="Genomics",
            description="Alpha Description",
            features=["sequence_analysis", "alignment"]
        )
        self.tool2 = Tool(
            tool_id=2,
            name="Beta",
            category="Proteomics",
            description="Beta Description",
            features=["mass_spectrometry", "protein_identification"]
        )
        self.tool3 = Tool(
            tool_id=3,
            name="Gamma",
            category="Genomics",
            description="Gamma Description",
            features=["variant_calling", "genome_assembly"]
        )
        self.tool4 = Tool(
            tool_id=4,
            name="Delta",
            category="Metabolomics",
            description="Delta Description",
            features=["metabolite_profiling", "pathway_analysis"]
        )

        self.tools = [self.tool1, self.tool2, self.tool3, self.tool4]

        self.tree = ToolTree()

    def test_initialization(self):
        """
        Test initializing the ToolTree.
        """
        self.assertIsInstance(self.tree.root, TreeNode)
        self.assertEqual(self.tree.root.name, "root")
        self.assertEqual(self.tree.root.original_name, "Root")
        self.assertEqual(self.tree.categories, {})
        self.assertEqual(self.tree.tools, [])

    def test_build_tree(self):
        """
        Test building the tree with a list of tools.
        """
        self.tree.build_tree(self.tools)
        self.assertEqual(len(self.tree.tools), 4)
        self.assertEqual(len(self.tree.categories), 3)  # Genomics, Proteomics, Metabolomics

        # Check if categories are added correctly
        self.assertIn("genomics", self.tree.categories)
        self.assertIn("proteomics", self.tree.categories)
        self.assertIn("metabolomics", self.tree.categories)

        # Check if tools are added under the correct categories
        genomics_node = self.tree.categories["genomics"]
        proteomics_node = self.tree.categories["proteomics"]
        metabolomics_node = self.tree.categories["metabolomics"]

        self.assertEqual(len(genomics_node.children), 2)  # Alpha and Gamma
        self.assertEqual(len(proteomics_node.children), 1)  # Beta
        self.assertEqual(len(metabolomics_node.children), 1)  # Delta

        # Verify tool details in categories
        self.assertEqual(genomics_node.children[0].tool, self.tool1)
        self.assertEqual(genomics_node.children[1].tool, self.tool3)
        self.assertEqual(proteomics_node.children[0].tool, self.tool2)
        self.assertEqual(metabolomics_node.children[0].tool, self.tool4)

    def test_add_tool_new_category(self):
        """
        Test adding a tool to a new category.
        """
        self.tree.add_tool(self.tool1)
        self.assertIn("genomics", self.tree.categories)
        genomics_node = self.tree.categories["genomics"]
        self.assertEqual(len(genomics_node.children), 1)
        self.assertEqual(genomics_node.children[0].tool, self.tool1)

    def test_add_tool_existing_category(self):
        """
        Test adding a tool to an existing category.
        """
        self.tree.add_tool(self.tool1)
        self.tree.add_tool(self.tool3)  # Same category as tool1
        self.assertEqual(len(self.tree.categories), 1)
        genomics_node = self.tree.categories["genomics"]
        self.assertEqual(len(genomics_node.children), 2)
        self.assertEqual(genomics_node.children[1].tool, self.tool3)

    def test_find_category_node_existing(self):
        """
        Test finding an existing category node.
        """
        self.tree.build_tree(self.tools)
        node = self.tree.find_category_node("Proteomics")
        self.assertIsNotNone(node)
        self.assertEqual(node.original_name, "Proteomics")

    def test_find_category_node_non_existing(self):
        """
        Test finding a non-existing category node.
        """
        self.tree.build_tree(self.tools)
        node = self.tree.find_category_node("NonExistentCategory")
        self.assertIsNone(node)

    def test_get_tools_in_category_existing(self):
        """
        Test retrieving tools in an existing category.
        """
        self.tree.build_tree(self.tools)
        tools_in_genomics = self.tree.get_tools_in_category("Genomics")
        self.assertEqual(len(tools_in_genomics), 2)
        self.assertIn(self.tool1, tools_in_genomics)
        self.assertIn(self.tool3, tools_in_genomics)

    def test_get_tools_in_category_non_existing(self):
        """
        Test retrieving tools in a non-existing category, expecting ValueError.
        """
        self.tree.build_tree(self.tools)
        with self.assertRaises(ValueError) as context:
            self.tree.get_tools_in_category("NonExistentCategory")
        self.assertIn("Category 'NonExistentCategory' not found.", str(context.exception))

    def test_search_tools_by_name(self):
        """
        Test searching tools by name.
        """
        self.tree.build_tree(self.tools)
        results = self.tree.search_tools("Alpha")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.tool1)

    def test_search_tools_by_description(self):
        """
        Test searching tools by description.
        """
        self.tree.build_tree(self.tools)
        results = self.tree.search_tools("protein_identification")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.tool2)

    def test_search_tools_by_category(self):
        """
        Test searching tools by category.
        """
        self.tree.build_tree(self.tools)
        results = self.tree.search_tools("genomics")
        self.assertEqual(len(results), 2)
        self.assertIn(self.tool1, results)
        self.assertIn(self.tool3, results)

    def test_search_tools_by_features(self):
        """
        Test searching tools by features.
        """
        self.tree.build_tree(self.tools)
        results = self.tree.search_tools("alignment")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.tool1)

    def test_search_tools_partial_match(self):
        """
        Test searching tools with a partial keyword.
        """
        self.tree.build_tree(self.tools)
        results = self.tree.search_tools("mass")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.tool2)

    def test_search_tools_no_matches(self):
        """
        Test searching tools with a keyword that has no matches.
        """
        self.tree.build_tree(self.tools)
        results = self.tree.search_tools("NonExistentKeyword")
        self.assertEqual(len(results), 0)

    def test_search_tools_case_insensitive(self):
        """
        Test that search_tools is case-insensitive.
        """
        self.tree.build_tree(self.tools)
        results_upper = self.tree.search_tools("ALPHA")
        results_mixed = self.tree.search_tools("AlPhA")
        self.assertEqual(len(results_upper), 1)
        self.assertEqual(len(results_mixed), 1)
        self.assertEqual(results_upper[0], self.tool1)
        self.assertEqual(results_mixed[0], self.tool1)

    def test_get_all_categories(self):
        """
        Test retrieving all categories with original casing.
        """
        self.tree.build_tree(self.tools)
        categories = self.tree.get_all_categories()
        expected_categories = ["Genomics", "Proteomics", "Metabolomics"]
        self.assertEqual(set(categories), set(expected_categories))

    def test_traverse_tree(self):
        """
        Test traversing the tree and verifying printed output.
        """
        self.tree.build_tree(self.tools)
        expected_output = (
            "- Root\n"
            "    - Genomics\n"
            "        - Alpha\n"
            "        - Gamma\n"
            "    - Proteomics\n"
            "        - Beta\n"
            "    - Metabolomics\n"
            "        - Delta\n"
        )

        with patch('builtins.print') as mock_print:
            self.tree.traverse_tree()
            # Capture all print calls
            printed = ""
            for call in mock_print.call_args_list:
                args, _ = call
                printed += args[0] + "\n"

            # Compare printed output
            self.assertEqual(printed, expected_output)

    def test_traverse_tree_from_subnode(self):
        """
        Test traversing the tree starting from a subnode.
        """
        self.tree.build_tree(self.tools)
        genomics_node = self.tree.find_category_node("Genomics")
        expected_output = (
            "- Genomics\n"
            "    - Alpha\n"
            "    - Gamma\n"
        )

        with patch('builtins.print') as mock_print:
            self.tree.traverse_tree(node=genomics_node)
            # Capture all print calls
            printed = ""
            for call in mock_print.call_args_list:
                args, _ = call
                printed += args[0] + "\n"

            # Compare printed output
            self.assertEqual(printed, expected_output)


class TestToolTreeEdgeCases(unittest.TestCase):
    """
    Test cases for ToolTree focusing on edge cases.
    """

    def setUp(self):
        """
        Set up a ToolTree instance with sample tools for testing.
        """
        self.tool1 = Tool(
            tool_id=1,
            name="Alpha",
            category="Genomics",
            description="Alpha Description",
            features=["sequence_analysis", "alignment"]
        )
        self.tool2 = Tool(
            tool_id=2,
            name="Beta",
            category="Proteomics",
            description="Beta Description",
            features=["mass_spectrometry", "protein_identification"]
        )
        self.tool3 = Tool(
            tool_id=3,
            name="Gamma",
            category="Genomics",
            description="Gamma Description",
            features=["variant_calling", "genome_assembly"]
        )
        self.tool4 = Tool(
            tool_id=4,
            name="Delta",
            category="Metabolomics",
            description="Delta Description",
            features=["metabolite_profiling", "pathway_analysis"]
        )

        self.tools = [self.tool1, self.tool2, self.tool3, self.tool4]

        self.tree = ToolTree()

    def test_add_tool_case_insensitive_category(self):
        """
        Test adding tools with categories differing only in case.
        """
        tool_upper = Tool(
            tool_id=5,
            name="Epsilon",
            category="GENOMICS",  # Uppercase category
            description="Epsilon Description",
            features=["gene_editing"]
        )
        self.tree.add_tool(self.tool1)  # "Genomics"
        self.tree.add_tool(tool_upper)   # "GENOMICS"

        self.assertEqual(len(self.tree.categories), 1)
        genomics_node = self.tree.categories["genomics"]
        self.assertEqual(len(genomics_node.children), 2)
        self.assertIn(self.tool1, [child.tool for child in genomics_node.children])
        self.assertIn(tool_upper, [child.tool for child in genomics_node.children])

    def test_search_tools_with_empty_features(self):
        """
        Test searching tools where some tools have empty features.
        """
        tool_with_no_features = Tool(
            tool_id=5,
            name="Epsilon",
            category="Genomics",
            description="Epsilon Description",
            features=[]
        )
        self.tools.append(tool_with_no_features)
        self.tree.build_tree(self.tools)

        results = self.tree.search_tools("Epsilon")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], tool_with_no_features)

    def test_search_tools_with_overlapping_keywords(self):
        """
        Test searching tools with keywords that overlap in different fields.
        """
        tool_overlapping = Tool(
            tool_id=5,
            name="AlphaBeta",
            category="Genomics",
            description="Advanced mass spectrometry tool",
            features=["sequence_analysis", "mass_spectrometry"]
        )
        self.tools.append(tool_overlapping)
        self.tree.build_tree(self.tools)

        # Search by name
        results_name = self.tree.search_tools("Alpha")
        self.assertIn(self.tool1, results_name)
        self.assertIn(tool_overlapping, results_name)

        # Search by description
        results_description = self.tree.search_tools("mass")
        self.assertIn(self.tool2, results_description)
        self.assertIn(tool_overlapping, results_description)

        # Search by features
        results_features = self.tree.search_tools("mass_spectrometry")
        self.assertIn(self.tool2, results_features)
        self.assertIn(tool_overlapping, results_features)

    def test_search_tools_with_numeric_keywords(self):
        """
        Test searching tools with numeric keywords.
        """
        tool_numeric = Tool(
            tool_id=5,
            name="Gamma2",
            category="Genomics",
            description="Gamma version 2",
            features=["variant_calling2"]
        )
        self.tools.append(tool_numeric)
        self.tree.build_tree(self.tools)

        results = self.tree.search_tools("2")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], tool_numeric)


class TestToolTreeErrorHandling(unittest.TestCase):
    """
    Test cases for ToolTree focusing on error handling.
    """

    def setUp(self):
        """
        Set up a ToolTree instance without any tools for testing.
        """
        self.tree = ToolTree()

    def test_get_tools_in_category_empty_tree(self):
        """
        Test retrieving tools from a category when the tree is empty, expecting ValueError.
        """
        with self.assertRaises(ValueError) as context:
            self.tree.get_tools_in_category("Genomics")
        self.assertIn("Category 'Genomics' not found.", str(context.exception))

    def test_search_tools_empty_tree(self):
        """
        Test searching tools in an empty tree, expecting no results.
        """
        results = self.tree.search_tools("Alpha")
        self.assertEqual(len(results), 0)

    def test_get_all_categories_empty_tree(self):
        """
        Test retrieving all categories from an empty tree.
        """
        categories = self.tree.get_all_categories()
        self.assertEqual(len(categories), 0)

    def test_build_tree_with_empty_tools_list(self):
        """
        Test building the tree with an empty tools list.
        """
        self.tree.build_tree([])
        self.assertEqual(len(self.tree.tools), 0)
        self.assertEqual(len(self.tree.categories), 0)
        self.assertEqual(len(self.tree.root.children), 0)


class TestToolTreeRepeatedBuilds(unittest.TestCase):
    """
    Test cases for ToolTree focusing on building the tree multiple times.
    """

    def setUp(self):
        """
        Set up a ToolTree instance with initial tools.
        """
        self.tool1 = Tool(
            tool_id=1,
            name="Alpha",
            category="Genomics",
            description="Alpha Description",
            features=["sequence_analysis", "alignment"]
        )
        self.tool2 = Tool(
            tool_id=2,
            name="Beta",
            category="Proteomics",
            description="Beta Description",
            features=["mass_spectrometry", "protein_identification"]
        )
        self.tools_initial = [self.tool1, self.tool2]

        self.tree = ToolTree()
        self.tree.build_tree(self.tools_initial)

    def test_build_tree_multiple_times(self):
        """
        Test building the tree multiple times and ensure tools and categories are managed correctly.
        """
        self.assertEqual(len(self.tree.tools), 2)
        self.assertEqual(len(self.tree.categories), 2)

        # Add more tools
        tool3 = Tool(
            tool_id=3,
            name="Gamma",
            category="Genomics",
            description="Gamma Description",
            features=["variant_calling", "genome_assembly"]
        )
        tool4 = Tool(
            tool_id=4,
            name="Delta",
            category="Metabolomics",
            description="Delta Description",
            features=["metabolite_profiling", "pathway_analysis"]
        )
        tools_additional = [tool3, tool4]
        self.tree.build_tree(tools_additional)

        self.assertEqual(len(self.tree.tools), 4)
        self.assertEqual(len(self.tree.categories), 3)  # Genomics, Proteomics, Metabolomics

        # Verify tools in Genomics
        genomics_node = self.tree.categories["genomics"]
        self.assertEqual(len(genomics_node.children), 2)
        self.assertIn(self.tool1, [child.tool for child in genomics_node.children])
        self.assertIn(tool3, [child.tool for child in genomics_node.children])

        # Verify tools in Proteomics
        proteomics_node = self.tree.categories["proteomics"]
        self.assertEqual(len(proteomics_node.children), 1)
        self.assertIn(self.tool2, [child.tool for child in proteomics_node.children])

        # Verify tools in Metabolomics
        metabolomics_node = self.tree.categories["metabolomics"]
        self.assertEqual(len(metabolomics_node.children), 1)
        self.assertIn(tool4, [child.tool for child in metabolomics_node.children])


if __name__ == '__main__':
    unittest.main()
