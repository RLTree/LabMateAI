# collaborative_recommender.py

"""
collaborative_recommender.py

This module provides the CollaborativeRecommender class, which implements
user-based collaborative filtering using the NearestNeighbors algorithm.
It generates tool recommendations for users based on the preferences of similar users.

Classes:
    CollaborativeRecommender: Implements user-based collaborative filtering.
"""

import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors


class CollaborativeRecommender:
    """
    Implements user-based collaborative filtering using the NearestNeighbors algorithm.
    """

    def __init__(self, user_item_matrix: pd.DataFrame, tools_df: pd.DataFrame, n_neighbors: int = 5):
        """
        Initializes the CollaborativeRecommender.

        Args:
            user_item_matrix (pd.DataFrame): The user-item rating matrix where rows represent users,
                                             columns represent tools, and values represent ratings.
            tools_df (pd.DataFrame): The DataFrame containing tool details with at least 'tool_id' and 'tool_name' columns.
            n_neighbors (int): The number of similar users to consider for generating recommendations.

        Raises:
            ValueError: If n_neighbors is less than 1.
            ValueError: If user_item_matrix contains tool_ids not present in tools_df.
        """
        # Convert user_item_matrix to float type to ensure compatibility with NearestNeighbors
        self.user_item_matrix = user_item_matrix.astype(float)
        self.tools_df = tools_df
        self.n_neighbors = n_neighbors

        # Validate that all tool_ids in user_item_matrix are present in tools_df
        tool_ids_in_matrix = set(user_item_matrix.columns)
        tool_ids_in_tools_df = set(tools_df['tool_id'])
        missing_tool_ids = tool_ids_in_matrix - tool_ids_in_tools_df
        if missing_tool_ids:
            raise ValueError(
                f"User-item matrix contains tool_ids not present in tools_df: {missing_tool_ids}")

        # Validate unique tool IDs in tools_df
        if tools_df['tool_id'].duplicated().any():
            raise ValueError("Duplicate tool_ids found in tools_df.")

        if n_neighbors < 1:
            raise ValueError("n_neighbors must be at least 1.")

        # Validate that user_item_matrix's columns match tools_df's tool_id
        user_tool_ids = set(self.user_item_matrix.columns)
        tools_tool_ids = set(self.tools_df['tool_id'].unique())

        if not user_tool_ids.issubset(tools_tool_ids):
            missing_tools = user_tool_ids - tools_tool_ids
            raise ValueError(
                f"User-item matrix contains tool_ids not present in tools_df: {missing_tools}")

        # Initialize the NearestNeighbors model with cosine similarity
        self.model = NearestNeighbors(metric='cosine', algorithm='brute')
        self.model.fit(self.user_item_matrix)

        # Create a mapping from tool_id to tool details for quick lookup
        self.tool_id_to_details = self.tools_df.set_index(
            'tool_id').to_dict('index')

        # Create a set of all tool_ids for validation
        self.all_tool_ids = set(self.tools_df['tool_id'].unique())

    def get_recommendations(self, user_id: int, n_recommendations: int = 5) -> list:
        """
        Generates tool recommendations for a given user based on similar users' preferences.

        Args:
            user_id (int): The ID of the user to generate recommendations for.
            n_recommendations (int): The number of tool recommendations to generate.

        Returns:
            list: A list of recommended tools as dictionaries containing tool details.

        Raises:
            ValueError: If the user_id is not found in the user-item matrix.
            ValueError: If n_recommendations is less than 1.
        """
        if n_recommendations < 1:
            raise ValueError("n_recommendations must be at least 1.")

        if user_id not in self.user_item_matrix.index:
            raise ValueError(
                f"User ID {user_id} not found in the user-item matrix.")

        # Retrieve the user's ratings vector
        user_vector = self.user_item_matrix.loc[user_id].values.reshape(1, -1)

        # Chech if user has rated any tools
        if np.all(user_vector == 0.0):
            tool_ratings = self.user_item_matrix.mean().sort_values(ascending=False)
            top_recommendations = tool_ratings.head(n_recommendations)
            recommended_tools = self.tools_df[self.tools_df['tool_id'].isin(
                top_recommendations.index)]
            return recommended_tools.to_dict('records')

        # Check if user has rated all tools
        if np.all(user_vector != 0.0):
            recommended_tools = []
            return recommended_tools

        # Ensure we have enough samples for neighbors
        n_neighbors = min(self.n_neighbors, len(self.user_item_matrix))

        # Find the nearest neighbors (similar users)
        distances, indices = self.model.kneighbors(
            user_vector, n_neighbors=self.n_neighbors + 1)  # +1 to include the user itself

        # Exclude the user itself
        similar_users_indices = indices.flatten()[1:]

        # Aggregate ratings from similar users
        similar_users_ratings = self.user_item_matrix.iloc[similar_users_indices]
        mean_ratings = similar_users_ratings.mean(axis=0)

        # Identify tools the user has already interacted with
        user_rated_tools = set(
            self.user_item_matrix.loc[user_id][self.user_item_matrix.loc[user_id] > 0].index)

        # Exclude already rated tools from recommendations
        potential_recommendations = mean_ratings.drop(
            labels=user_rated_tools, errors='ignore')

        # Sort the potential recommendations by descending mean rating
        sorted_recommendations = potential_recommendations.sort_values(
            ascending=False)

        # Select the top N recommendations
        top_tool_ids = sorted_recommendations.head(
            n_recommendations).index.tolist()

        # Retrieve tool details from the tools_df
        recommended_tools = []
        for tool_id in top_tool_ids:
            if tool_id in self.tool_id_to_details:
                tool_details = self.tool_id_to_details[tool_id]
                recommended_tool = {
                    'tool_id': tool_id,
                    'tool_name': tool_details['tool_name'],
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

    def __repr__(self):
        """
        Returns a string representation of the CollaborativeRecommender.

        Returns:
            str: A string describing the recommender and its configuration.
        """
        return (f"CollaborativeRecommender(n_neighbors={self.n_neighbors}, "
                f"number_of_tools={len(self.all_tool_ids)})")
