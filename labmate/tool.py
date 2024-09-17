"""
This module defines a Tool class that represents a tool with various attributes."""


class Tool:
    """A class representing a tool. Each tool has attributes: name, category, features, and cost."""

    def __init__(self, name, category, features, cost, description=None, url=None):
        """
        Initializes a Tool instance.

        Args:
            name (str): The name of the tool.
            category (str): The category of the tool.
            features (list): A list of features of the tool.
            cost (float): The cost of the tool.
            description (str, optional): A description of the tool. Defaults to None.
            url (str, optional): A URL for more information about the tool. Defaults to None.
        """
        self.name = name
        self.category = category
        self.features = features
        self.cost = cost
        self.description = description
        self.url = url

    def matches_criteria(self, criteria):
        """
        Checks if the tool matches the given criteria.

        Args:
            criteria (dict): A dictionary of criteria to match against.

        Returns:
            bool: True if the tool matches the criteria, False otherwise.
        """
        for key, value in criteria.items():
            if getattr(self, key, None) != value:
                return False
        return True

    def __repr__(self):
        """
        Returns a string representation of the tool instance.
        """
        return f'Tool({self.name}, {self.category}, {self.cost})'

    def __str__(self):
        """
        Returns a string representation of the tool.
        """
        return f'Tool: {self.name}, Category: {self.category}, Cost: {self.cost}, Features: {self.features}'
