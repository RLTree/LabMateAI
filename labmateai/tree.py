"""
This module defines a tree structure to organize tools by categories.
"""


class TreeNode:
    """
    A class representing a node in a tree data structure.

    Attributes:
        name (str): The name of the node.
        tool (object): The tool associated with the node (optional).
        children (list): A list of child nodes.
    """

    def __init__(self, name, tool=None, original_name=None):
        self.name = name  # Normalized name (e.g., lowercase)
        self.original_name = original_name or name  # Original name
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
        self.categories = {}

    def build_tree(self, tools):
        """
        Builds the tool tree from a list of tools.

        Args:
            tools (list): A list of Tool objects.
        """
        for tool in tools:
            self.add_tool(tool)

    def add_tool(self, tool):
        """
        Adds a tool to the tree under the specified category.

        Args:
            tool: The tool to add.
        """
        normalized_category = tool.category.lower()
        if normalized_category not in self.categories:
            category_node = TreeNode(
                normalized_category, original_name=tool.category)
            self.root.add_child(category_node)
            self.categories[normalized_category] = category_node
        else:
            category_node = self.categories[normalized_category]
        category_node.add_child(TreeNode(tool.name, tool))

    def find_category_node(self, category_name):
        """
        Finds the category node in the tree.

        Args:
            category_name (str): The name of the category to find.

        Returns:
            TreeNode: The category node if found, None otherwise.
        """
        normalized_category = category_name.lower()
        return self.categories.get(normalized_category)

    def get_tools_in_category(self, category_name):
        """
        Retrieves all tools in a specified category.

        Args:
            category_name (str): The name of the category to retrieve tools from.

        Returns:
            list: A list of tools in the specified category.

        Raises:
            ValueError: If the category does not exist.
        """
        category_node = self.find_category_node(category_name)
        if category_node:
            return [child.tool for child in category_node.children if child.tool]
        else:
            raise ValueError(f"Category '{category_name}' not found.")

    def search_tools(self, keyword):
        """
        Searches for tools that match the provided keyword in their name, description, or features.

        Args:
            keyword (str): The keyword to search for.

        Returns:
            list: A list of matching tools.
        """
        results = []
        keyword_lower = keyword.lower()

        def search_node(node):
            if node.tool:
                tool = node.tool
                if (keyword_lower in tool.name.lower() or
                    keyword_lower in tool.description.lower() or keyword_lower in tool.category.lower() or
                        any(keyword_lower in feature.lower() for feature in tool.features)):
                    results.append(tool)
            for child in node.children:
                search_node(child)

        search_node(self.root)
        return results

    def get_all_categories(self):
        """
        Returns a list of all categories in the tree.
        """
        return [node.original_name for node in self.categories.values()]

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
