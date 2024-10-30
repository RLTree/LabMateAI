# labmateai/hybrid_recommender.py

"""
Hybrid Recommender Module for LabMateAI

This module provides the HybridRecommender class, which combines content-based and collaborative filtering
to generate comprehensive tool recommendations for users. It adheres to the RecommenderInterface,
ensuring consistency across different recommender systems.
"""

import pandas as pd
from typing import List, Dict, Optional
from .recommender_interface import RecommenderInterface
from .collaborative_recommender import CollaborativeRecommender
from .content_based_recommender import ContentBasedRecommender


class HybridRecommender(RecommenderInterface):
    """
    Implements a hybrid filtering approach combining content-based and collaborative filtering.
    """

    def __init__(
        self,
        content_recommender: ContentBasedRecommender,
        collaborative_recommender: CollaborativeRecommender,
        alpha: float = 0.5
    ):
        """
        Initializes the HybridRecommender.

        Args:
            content_recommender (ContentBasedRecommender): The content-based recommender instance.
            collaborative_recommender (CollaborativeRecommender): The collaborative filtering recommender instance.
            alpha (float, optional): The weighting factor for combining CF and CBF scores (0 <= alpha <= 1).
                Defaults to 0.5.

        Raises:
            ValueError: If alpha is not between 0 and 1.
        """
        super().__init__()
        if not (0 <= alpha <= 1):
            raise ValueError("Alpha must be between 0 and 1.")

        self.content_recommender = content_recommender
        self.collaborative_recommender = collaborative_recommender
        self.alpha = alpha

    def recommend(
        self,
        user_id: Optional[int] = None,
        tool_name: Optional[str] = None,
        num_recommendations: int = 5
    ) -> List[Dict]:
        """
        Generates hybrid recommendations for a user by combining collaborative filtering and content-based filtering scores.

        Args:
            user_id (Optional[int]): The ID of the user for personalized recommendations.
                If provided, collaborative filtering is utilized.
            tool_name (Optional[str]): Name of the tool for content-based recommendations.
                If provided, content-based filtering is utilized.
            num_recommendations (int, optional): Number of recommendations to generate.
                Defaults to 5.

        Returns:
            List[Dict]: A list of recommended tools with their details.

        Raises:
            ValueError: If num_recommendations is less than 1.
            ValueError: If neither user_id nor tool_name is provided.
        """
        if num_recommendations < 1:
            raise ValueError("num_recommendations must be at least 1.")
        if user_id is None and tool_name is None:
            raise ValueError("At least one of user_id or tool_name must be provided for recommendations.")

        # Obtain collaborative filtering scores if user_id is provided
        if user_id is not None:
            try:
                collaborative_scores = self._get_collaborative_scores(user_id)
            except ValueError as e:
                raise ValueError(f"Collaborative filtering error: {e}")
        else:
            # If no user_id is provided, use zero scores
            collaborative_scores = pd.Series(0, index=self.collaborative_recommender.tools_df['tool_id'])

        # Obtain content-based filtering scores if tool_name is provided
        if tool_name is not None:
            try:
                content_scores = self._get_content_scores(tool_name)
            except ValueError as e:
                raise ValueError(f"Content-based filtering error: {e}")
        else:
            # If no tool_name is provided, use zero scores
            content_scores = pd.Series(0, index=self.content_recommender.tools_df['tool_id'])

        # Align indices
        combined_index = self._align_indices(collaborative_scores, content_scores)
        collaborative_scores = collaborative_scores.reindex(combined_index, fill_value=0)
        content_scores = content_scores.reindex(combined_index, fill_value=0)

        # Normalize the scores
        normalized_cf_scores = self._normalize_scores(collaborative_scores)
        normalized_cb_scores = self._normalize_scores(content_scores)

        # Combine the scores using the weighting factor alpha
        combined_scores = self.alpha * normalized_cf_scores + (1 - self.alpha) * normalized_cb_scores

        # Sort the tools based on the combined scores in descending order
        top_tool_ids = combined_scores.sort_values(ascending=False).head(num_recommendations).index

        # Retrieve the tool details from collaborative_recommender's tools_df
        recommended_tools = self.collaborative_recommender.tools_df[
            self.collaborative_recommender.tools_df['tool_id'].isin(top_tool_ids)
        ]

        return recommended_tools.to_dict('records')

    def get_recommendation_scores(self, identifier: str) -> Dict[int, float]:
        """
        Retrieve recommendation scores based on a user ID or tool name.

        Args:
            identifier (str): The identifier for generating scores. It can be a user ID (as a string)
                or a tool name.

        Returns:
            Dict[int, float]: A dictionary mapping tool IDs to their corresponding recommendation scores.

        Raises:
            ValueError: If the identifier is neither a valid user ID nor a valid tool name.
        """
        # Attempt to interpret identifier as user_id
        try:
            user_id = int(identifier)
            scores = self._get_collaborative_scores(user_id)
            return scores.to_dict()
        except ValueError:
            # If not an integer, treat it as tool_name
            scores = self._get_content_scores(identifier)
            return scores.to_dict()

    def display_recommendations(self, recommendations: List[Dict]) -> None:
        """
        Display the list of recommended tools to the user in a readable format.

        Args:
            recommendations (List[Dict]): A list of recommended tools, each represented as a dictionary.
        """
        if not recommendations:
            print("No recommendations found.")
            return

        print("Recommended Tools:")
        for tool in recommendations:
            print(f"- {tool['name']} (Category: {tool['category']}, Language: {tool['language']}, Platform: {tool['platform']})")

    def _get_collaborative_scores(self, user_id: int) -> pd.Series:
        """
        Retrieves collaborative filtering scores for all tools for a given user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            pd.Series: A Series with tool_ids as index and collaborative scores as values.

        Raises:
            ValueError: If user_id is not found in the collaborative recommender.
        """
        return self.collaborative_recommender.get_recommendation_scores(user_id)

    def _get_content_scores(self, tool_name: str) -> pd.Series:
        """
        Retrieves content-based filtering scores for all tools based on a reference tool.

        Args:
            tool_name (str): The name of the tool to base content scores on.

        Returns:
            pd.Series: A Series with tool_ids as index and content-based scores as values.

        Raises:
            ValueError: If tool_name is not found in the content recommender.
        """
        return self.content_recommender.get_recommendation_scores(tool_name)

    def _normalize_scores(self, scores: pd.Series) -> pd.Series:
        """
        Normalizes a Series of scores to a range between 0 and 1.

        Args:
            scores (pd.Series): The scores to normalize.

        Returns:
            pd.Series: The normalized scores.

        Notes:
            If all scores are equal, the normalized scores will be zero to avoid division by zero.
        """
        min_score = scores.min()
        max_score = scores.max()
        if max_score - min_score == 0:
            return pd.Series(0, index=scores.index)
        return (scores - min_score) / (max_score - min_score)

    def _align_indices(self, series1: pd.Series, series2: pd.Series) -> pd.Index:
        """
        Aligns two pandas Series to have the same index.

        Args:
            series1 (pd.Series): The first Series.
            series2 (pd.Series): The second Series.

        Returns:
            pd.Index: The combined index of both Series.
        """
        return series1.index.union(series2.index)

    def __repr__(self) -> str:
        """
        Returns a string representation of the HybridRecommender.

        Returns:
            str: String representation.
        """
        return (
            f"HybridRecommender(alpha={self.alpha}, "
            f"content_recommender={repr(self.content_recommender)}, "
            f"collaborative_recommender={repr(self.collaborative_recommender)})"
        )
