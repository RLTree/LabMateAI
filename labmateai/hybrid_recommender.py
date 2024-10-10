# hybrid_recommender.py

"""
This module provides the HybridRecommender class, which combines content-based and collaborative filtering
to generate hybrid recommendations for users.
"""


import pandas as pd
from .collaborative_recommender import CollaborativeRecommender
from .recommender import Recommender


class HybridRecommender:
    """
    Implements a hybrid filtering approach combining content-based and collaborative filtering.
    """

    def __init__(self, content_recommender: Recommender, collaborative_recommender: CollaborativeRecommender, alpha: float = 0.5):
        """
        Initializes the hybrid recommender.

        Args:
            content_recommender (Recommender): The content-based recommender instance.
            collaborative_recommender (CollaborativeRecommender): The collaborative filtering recommender instance.
            alpha (float): The weighting factor for combining CF and CBF scores (0 <= alpha <= 1).
        """
        self.content_recommender = content_recommender
        self.collaborative_recommender = collaborative_recommender
        self.alpha = alpha

    def recommend(self, user_id: int, tool_name: str = None, num_recommendations: int = 5) -> list:
        """
        Generates hybrid recommendations for a user.

        Args:
            user_id (int): The ID of the user.
            tool_name (str): Name of the tool for content-based recommendations.
            num_recommendations (int): Number of recommendations to generate.

        Returns:
            list: A list of recommended tools.
        """
        # Get collaborative filtering recommendation scores
        collaborative_scores = self.collaborative_recommender.get_recommendation_scores(
            user_id)

        # Get content-based recommendation scores if a tool is provided
        if tool_name:
            content_scores = self.content_recommender.get_recommendation_scores(
                tool_name)
        else:
            content_scores = pd.Series(0, index=collaborative_scores.index)

        # Normalize scores to range [0, 1] for proper combination
        collaborative_scores = (collaborative_scores - collaborative_scores.min()) / (
            collaborative_scores.max() - collaborative_scores.min())
        content_scores = (content_scores - content_scores.min()) / \
            (content_scores.max() - content_scores.min())

        # Combine CF and CBF scores
        combined_scores = self.alpha * collaborative_scores + \
            (1 - self.alpha) * content_scores

        # Sort the tools by the combined scores and return the top recommendations
        top_tool_ids = combined_scores.sort_values(
            ascending=False).head(num_recommendations).index
        recommended_tools = self.collaborative_recommender.tools_df[self.collaborative_recommender.tools_df['tool_id'].isin(
            top_tool_ids)]

        return recommended_tools.to_dict('records')
