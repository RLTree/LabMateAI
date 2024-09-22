"""
This module defines a tree structure to organize tools by categories.
"""


class TreeNode:
    """
    A class representing a node in a tree data structure.

    Attributes:
        name (str): The name of the node.
        tool (str): The tool associated with the node (optional).
        children (list): A list of child nodes.
    """

    def __init__(self, name, tool=None):
        self.name = name
        self.tool = tool
        self.children = []

    def add_child(self, child_node):
        """
        Adds a child node to the current node.
        """
        self.children.append(child_node)

    def is_leaf(self):
        """
        Check if the node is a leaf node.

        Returns:
            bool: True if the node has no children, False otherwise.
        """
        return len(self.children) == 0


class ToolTree:
    """
    A class to represent the tree structure for organizing tools by categories.
    """

    def __init__(self):
        self.root = TreeNode("Root")

    def build_tree(self, tools):
        """
        Builds the tool tree from a list of tools.

        Args:
            tools (list): A list of tuples where each tuple contains (category, tool_name).
        """
        for tool in tools:
            self.add_tool(tool)

    def add_tool(self, tool):
        """
        Adds a tool to the tree under the specified category.

        Args:
            tool: The tool to add.
        """
        category_node = self.find_category_node(tool.category)
        if category_node is None:
            category_node = TreeNode(tool.category)
            self.root.add_child(category_node)
        category_node.add_child(TreeNode(tool.name, tool))

    def find_category_node(self, category_name):
        """
        Finds the category node in the tree.

        Args:
            category_name (str): The name of the category to find.

        Returns:
            TreeNode: The category node if found, None otherwise.
        """
        if self.root.children:
            for child in self.root.children:
                if child.name == category_name:
                    return child

        return None

    def get_tools_in_category(self, category_name):
        """
        Retrieves all tools in a specified category.

        Args:
            category_name (str): The name of the category to retrieve tools from.

        Returns:
            list: A list of tools in the specified category.
        """
        category_node = self.find_category_node(category_name)
        if category_node:
            return [child.tool for child in category_node.children]
        return []

    def search_tools(self, keyword):
        """
        Searches for tools by keyword.

        Args:
            keyword (str): The keyword to search for.

        Returns:
            list: A list of tools matching the keyword.
        """

        matching_tools = []
        for category in self.root.children:
            for node in category.children:
                if keyword.lower() in node.name.lower() or keyword.lower() in node.tool.category.lower():
                    matching_tools.append(node.tool)
        return matching_tools

    def traverse_tree(self, node=None, level=0):
        """
        Traverses the tree and prints the nodes.

        Args:
            node (TreeNode): The current node to traverse. Defaults to the root node.
            level (int): The current level in the tree. Defaults to 0.

        Returns:
            Tree structure printed to the console.
        """

        if node is None:
            node = self.root

        indent = " " * (level * 4)
        print(f"{indent}- {node.name}")
        for child in node.children:
            self.traverse_tree(child, level + 1)
