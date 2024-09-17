class TreeNode:
    """
    A class representing a node in a tree data structure.

    Attributes
    ----------
    value : any
        The value stored in the node.
    children : list
        A list of child nodes.
    """

    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        """
        Adds a child node to the current node.

        Args:
            child_node (TreeNode): The child node to be added.
        """
        self.children.append(child_node)

    def __repr__(self):
        return f'TreeNode({self.value})'

    def __str__(self):
        return f'TreeNode with value: {self.value} and children: {self.children}'

    def is_leaf(self):
        """
        Checks if the node is a leaf node (i.e., has no children).

        Returns:
            bool: True if the node is a leaf, False otherwise.
        """
        return len(self.children) == 0

    def depth(self):
        """
        Calculates the depth of the node in the tree.

        Returns:
            int: The depth of the node.
        """
        if not self.children:
            return 0
        return 1 + max(child.depth() for child in self.children)

    def height(self):
        """
        Calculates the height of the node in the tree.

        Returns:
            int: The height of the node.
        """
        if self.is_leaf():
            return 0
        return 1 + max(child.height() for child in self.children)

    def find(self, value):
        """
        Searches for a node with the specified value in the tree.

        Args:
            value: The value to search for.

        Returns:
            TreeNode: The node with the specified value, or None if not found.
        """
        if self.value == value:
            return self
        for child in self.children:
            result = child.find(value)
            if result is not None:
                return result
        return None

    def __eq__(self, other):
        """
        Checks if two TreeNode instances are equal.

        Args:
            other: The other TreeNode instance to compare with.

        Returns:
            bool: True if the nodes are equal, False otherwise.
        """
        if not isinstance(other, TreeNode):
            return False
        return self.value == other.value and self.children == other.children

    def __hash__(self):
        """
        Returns a hash of the TreeNode instance.

        Returns:
            int: The hash value of the TreeNode.
        """
        return hash((self.value, tuple(self.children)))

    def __iter__(self):
        """
        Allows iteration over the children of the TreeNode.

        Yields:
            TreeNode: The child nodes of the TreeNode.
        """
        for child in self.children:
            yield child

    def traverse(self):
        """
        Traverses the tree in a pre-order manner.

        Yields:
            TreeNode: The current node during traversal.
        """
        yield self

        for child in self.children:
            yield from child.traverse()
