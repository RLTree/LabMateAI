# labmateai/recommenders/collaborative_recommender.py

"""
Collaborative Recommender Module for LabMateAI

This module provides the CollaborativeRecommender class, which implements collaborative filtering
to generate tool recommendations based on user interactions. It adheres to the RecommenderInterface,
ensuring consistency across different recommender systems.

Classes:
    CollaborativeRecommender: Generates tool recommendations based on user interactions.

Functions:
    load_data: (Optional) Function to load user, tool, and interaction data.
"""

import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from typing import List, Dict, Optional
from .recommender_interface import RecommenderInterface


class CollaborativeRecommender(RecommenderInterface):
    """
    Collaborative Filtering Recommender using k-Nearest Neighbors.

    This recommender suggests tools to users based on the preferences of similar users.
    It operates on a user-item interaction matrix and requires a DataFrame containing tool details.
    Implements the RecommenderInterface to ensure consistency across recommenders.
    """

    def __init__(
        self,
        user_item_matrix: pd.DataFrame,
        tools_df: pd.DataFrame,
        n_neighbors: int = 5,
        metric: str = 'cosine',
        algorithm: str = 'brute'
    ):
        """
        Initializes the CollaborativeRecommender.

        Args:
            user_item_matrix (pd.DataFrame): A DataFrame where rows represent users,
                columns represent tool IDs, and values represent ratings.
            tools_df (pd.DataFrame): A DataFrame containing tool details with a 'tool_id' column.
            n_neighbors (int, optional): Number of similar users to consider. Defaults to 5.
            metric (str, optional): Distance metric for NearestNeighbors. Defaults to 'cosine'.
            algorithm (str, optional): Algorithm to compute nearest neighbors. Defaults to 'brute'.

        Raises:
            ValueError: If user_item_matrix is empty.
            ValueError: If tool_ids in user_item_matrix are not present in tools_df.
            ValueError: If there are duplicate tool_ids in tools_df.
            ValueError: If n_neighbors is less than 1.
        """
        super().__init__()

        self.user_item_matrix = user_item_matrix.astype(float)
        self.tools_df = tools_df

        self._validate_inputs(n_neighbors)
        self.n_neighbors = min(n_neighbors, len(user_item_matrix))

        self.tool_id_to_details = self.tools_df.set_index('tool_id').to_dict('index')
        self.all_tool_ids = set(self.tools_df['tool_id'].unique())

        self.model = NearestNeighbors(
            metric=metric,
            algorithm=algorithm,
            n_neighbors=self.n_neighbors
        )
        self.model.fit(self.user_item_matrix)

    def _validate_inputs(self, n_neighbors: int):
        """
        Validates the input data and parameters.

        Args:
            n_neighbors (int): Number of neighbors to validate.

        Raises:
            ValueError: If user_item_matrix is empty.
            ValueError: If tool_ids in user_item_matrix are not present in tools_df.
            ValueError: If there are duplicate tool_ids in tools_df.
            ValueError: If n_neighbors is less than 1.
        """
        if self.user_item_matrix.empty:
            raise ValueError("User-item matrix is empty. Cannot proceed with collaborative filtering.")

        tool_ids_in_matrix = set(self.user_item_matrix.columns)
        tool_ids_in_tools_df = set(self.tools_df['tool_id'])
        missing_tool_ids = tool_ids_in_matrix - tool_ids_in_tools_df
        if missing_tool_ids:
            raise ValueError(
                f"User-item matrix contains tool_ids not present in tools_df: {missing_tool_ids}"
            )

        if self.tools_df['tool_id'].duplicated().any():
            duplicated_ids = self.tools_df[self.tools_df['tool_id'].duplicated()]['tool_id'].unique()
            raise ValueError(f"Duplicate tool_ids found in tools_df: {duplicated_ids}")

        if n_neighbors < 1:
            raise ValueError("n_neighbors must be at least 1.")

    def recommend(
        self,
        user_id: Optional[int] = None,
        tool_name: Optional[str] = None,
        num_recommendations: int = 5
    ) -> List[Dict]:
        """
        Provides tool recommendations based on a user ID.

        Args:
            user_id (Optional[int], optional): The ID of the user for personalized recommendations.
                If provided, collaborative filtering is utilized.
            tool_name (Optional[str], optional): Not utilized in collaborative filtering.
                Can be provided for interface consistency but is ignored.
            num_recommendations (int, optional): Number of recommendations to generate.
                Defaults to 5.

        Returns:
            List[Dict]: A list of recommended tools with their details.

        Raises:
            ValueError: If num_recommendations is less than 1.
            ValueError: If user_id is not provided.
            ValueError: If user_id is not found in user_item_matrix.
        """
        if num_recommendations < 1:
            raise ValueError("num_recommendations must be at least 1.")
        if user_id is None:
            raise ValueError("user_id must be provided for collaborative recommendations.")

        if user_id not in self.user_item_matrix.index:
            raise ValueError(f"User ID {user_id} not found in the user-item matrix.")

        # Get recommendation scores
        scores = self.get_recommendation_scores(user_id)

        # Sort the scores in descending order
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

        # Get the tool IDs the user has already rated
        user_rated_tools = set(
            self.user_item_matrix.loc[user_id][self.user_item_matrix.loc[user_id] > 0].index
        )

        # Exclude tools already rated by the user
        sorted_scores = [item for item in sorted_scores if item[0] not in user_rated_tools]

        # Get the top N tool IDs
        top_tool_ids = [tool_id for tool_id, score in sorted_scores[:num_recommendations]]

        # Retrieve tool details
        recommended_tools = []
        for tool_id in top_tool_ids:
            if tool_id in self.tool_id_to_details:
                tool_details = self.tool_id_to_details[tool_id]
                recommended_tool = {
                    'tool_id': tool_id,
                    'tool_name': tool_details.get('name', ''),
                    'category': tool_details.get('category', ''),
                    'features': tool_details.get('features', ''),
                    'cost': tool_details.get('cost', ''),
                    'description': tool_details.get('description', ''),
                    'url': tool_details.get('url', ''),
                    'language': tool_details.get('language', ''),
                    'platform': tool_details.get('platform', '')
                }
                recommended_tools.append(recommended_tool)

        return recommended_tools

    def get_recommendation_scores(self, identifier: str) -> Dict[int, float]:
        """
        Retrieve recommendation scores based on a user ID.

        Args:
            identifier (str): The identifier for generating scores. It should be a user ID represented as a string.

        Returns:
            Dict[int, float]: A dictionary mapping tool IDs to their corresponding scores.

        Raises:
            ValueError: If the identifier cannot be converted to an integer user ID.
            ValueError: If the user ID is not found in user_item_matrix.
        """
        try:
            user_id = int(identifier)
        except ValueError:
            raise ValueError("Identifier must be a valid user ID represented as a string.")

        if user_id not in self.user_item_matrix.index:
            raise ValueError(f"User ID {user_id} not found in the user-item matrix.")

        return self.get_recommendation_scores_by_user(user_id)

    def get_recommendation_scores_by_user(self, user_id: int) -> Dict[int, float]:
        """
        Computes recommendation scores for all tools based on similar users.

        Args:
            user_id (int): The ID of the user to generate recommendations for.

        Returns:
            Dict[int, float]: A dictionary mapping tool IDs to their corresponding average ratings.
        """
        user_vector = self.user_item_matrix.loc[user_id].values.reshape(1, -1)

        # Handle users with no ratings
        if np.all(user_vector == 0.0):
            mean_ratings = self.user_item_matrix.mean(axis=0)
            return mean_ratings.to_dict()

        distances, indices = self.model.kneighbors(user_vector, n_neighbors=self.n_neighbors)
        similar_users_indices = indices.flatten()
        similar_users_ratings = self.user_item_matrix.iloc[similar_users_indices]
        mean_ratings = similar_users_ratings.mean(axis=0)

        return mean_ratings.to_dict()

    def display_recommendations(self, recommendations: List[Dict]) -> None:
        """
        Display the list of recommended tools to the user in a readable format.
        Adheres to the RecommenderInterface.

        Args:
            recommendations (List[Dict]): A list of recommended tools, each represented as a dictionary.
        """
        if not recommendations:
            print("No recommendations found.")
            return

        print("\nRecommended Tools:")
        for tool in recommendations:
            print(
                f"- {tool['tool_name']} - {tool['description']} "
                f"(Category: {tool['category']}, Cost: ${tool['cost']})"
            )

    def __repr__(self) -> str:
        """
        Returns a string representation of the CollaborativeRecommender.

        Returns:
            str: String representation.
        """
        return (
            f"CollaborativeRecommender(n_neighbors={self.n_neighbors}, "
            f"number_of_tools={len(self.all_tool_ids)})"
        )
