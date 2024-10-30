# labmateai/recommender_interface.py

"""
Recommender Interface Module for LabMateAI

This module defines the RecommenderInterface abstract base class, which serves as a contract
for all recommender systems within LabMateAI. Any concrete recommender must implement the
methods defined in this interface.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class RecommenderInterface(ABC):
    """
    Abstract Base Class for Recommender Systems.

    Defines the essential methods that any recommender system must implement.
    """

    @abstractmethod
    def recommend(
        self,
        user_id: Optional[int] = None,
        tool_name: Optional[str] = None,
        num_recommendations: int = 5
    ) -> List[Dict]:
        """
        Generate a list of recommended tools based on the provided parameters.

        Args:
            user_id (Optional[int]): The ID of the user for personalized recommendations.
                If provided, collaborative filtering methods may be used.
            tool_name (Optional[str]): The name of a tool to base content-based recommendations on.
                If provided, content-based filtering methods may be used.
            num_recommendations (int, optional): The number of recommendations to generate.
                Defaults to 5.

        Returns:
            List[Dict]: A list of recommended tools, each represented as a dictionary containing tool details.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        pass

    @abstractmethod
    def get_recommendation_scores(self, identifier: str) -> Dict[int, float]:
        """
        Retrieve recommendation scores for all tools based on a user ID or tool name.

        Args:
            identifier (str): The identifier for generating scores. It can be a user ID (as a string)
                or a tool name.

        Returns:
            Dict[int, float]: A dictionary mapping tool IDs to their corresponding recommendation scores.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        pass

    @abstractmethod
    def display_recommendations(self, recommendations: List[Dict]) -> None:
        """
        Display the list of recommended tools to the user in a readable format.

        Args:
            recommendations (List[Dict]): A list of recommended tools, each represented as a dictionary.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        pass

    def __repr__(self) -> str:
        """
        Return a string representation of the recommender.

        Returns:
            str: String representation of the recommender.
        """
        return f"{self.__class__.__name__}()"
