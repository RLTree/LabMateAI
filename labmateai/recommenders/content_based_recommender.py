# labmateai/recommenders/content_based_recommender.py

"""
Content-Based Recommender Module for LabMateAI

This module provides the ContentBasedRecommender class, which utilizes content-based
filtering techniques to recommend tools based on their attributes and similarities.
It adheres to the RecommenderInterface, ensuring consistency across different recommender systems.
"""

import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from typing import List, Dict, Optional
from .recommender_interface import RecommenderInterface
from ..graph import Graph
from ..tree import ToolTree
from ..tool import Tool


def load_data():
    """
    Load tool, user, and interaction data from CSV files.

    Returns:
        tuple: A tuple containing DataFrames for users, tools, and interactions.
    """
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct absolute paths to the CSV files
    users_path = os.path.join(script_dir, 'data', 'users.csv')
    tools_path = os.path.join(script_dir, 'data', 'tools.csv')
    interactions_path = os.path.join(script_dir, 'data', 'interactions.csv')

    # Load the CSV files
    users = pd.read_csv(users_path)
    tools = pd.read_csv(tools_path)
    interactions = pd.read_csv(interactions_path)
    return users, tools, interactions


def build_user_item_matrix(interactions: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a user-item matrix where rows represent users,
    columns represent tools, and values represent ratings.

    Args:
        interactions (pd.DataFrame): The interactions DataFrame.

    Returns:
        pd.DataFrame: The user-item matrix.
    """
    user_item_matrix = interactions.pivot_table(
        index='user_id',
        columns='tool_id',
        values='rating'
    ).fillna(0)
    return user_item_matrix


class ContentBasedRecommender(RecommenderInterface):
    """
    Handles content-based recommendations using Graph and ToolTree.
    Implements the RecommenderInterface to ensure consistency across recommenders.
    """

    def __init__(
        self,
        tools: List[Tool],
        graph: Optional[Graph] = None,
        tree: Optional[ToolTree] = None
    ):
        """
        Initializes the ContentBasedRecommender with a list of tools.

        Args:
            tools (List[Tool]): A list of Tool objects to be used for recommendations.
            graph (Optional[Graph], optional): An instance of Graph for managing tool similarities.
                If None, a new Graph instance is created. Defaults to None.
            tree (Optional[ToolTree], optional): An instance of ToolTree for hierarchical tool organization.
                If None, a new ToolTree instance is created. Defaults to None.

        Raises:
            ValueError: If duplicate tool IDs are found.
        """
        super().__init__()

        # Check for duplicate tool IDs
        tool_ids = set()
        for tool in tools:
            if tool.tool_id in tool_ids:
                raise ValueError(
                    f"Tool '{tool.name}' already exists in the dataset."
                )
            tool_ids.add(tool.tool_id)

        self.tools = tools
        self.graph = graph if graph else Graph(tools)
        self.tree = tree if tree else ToolTree()
        self.tool_names = {tool.name.lower() for tool in tools}  # For case-insensitive matching

        self.build_recommendation_system()

        # Preprocess tools for content-based filtering
        if tools:
            self.tools_df = pd.DataFrame([tool.__dict__ for tool in tools])
            self.tools_df['combined_features'] = self.tools_df.apply(
                lambda row: self._combine_features(row), axis=1
            )
            if not self.tools_df['combined_features'].empty:
                self.vectorizer = CountVectorizer().fit_transform(
                    self.tools_df['combined_features']
                )
                self.similarity_matrix = cosine_similarity(self.vectorizer)
            else:
                self.vectorizer = None
                self.similarity_matrix = None
        else:
            self.tools_df = pd.DataFrame()
            self.vectorizer = None
            self.similarity_matrix = None

    def _combine_features(self, row: pd.Series) -> str:
        """
        Combine selected features into a single string for each tool.

        Args:
            row (pd.Series): A row from the tools DataFrame.

        Returns:
            str: A string combining the features for content-based similarity calculations.
        """
        # Combine name, category, features, language, and platform into a single string
        combined = f"{row['name']} {row['category']} {' '.join(row['features'])} {row['language']} {row['platform']}"
        return combined

    def build_recommendation_system(self) -> None:
        """
        Builds the recommendation system by constructing the graph and tree.
        """
        self.graph.build_graph(self.tools)
        self.tree.build_tree(self.tools)

    def recommend(
        self,
        user_id: Optional[int] = None,
        tool_name: Optional[str] = None,
        num_recommendations: int = 5
    ) -> List[Dict]:
        """
        Provides recommendations based on the input parameters.
        Adheres to the RecommenderInterface.

        Args:
            user_id (Optional[int], optional): The ID of the user for personalized recommendations.
                If provided, collaborative filtering is utilized.
            tool_name (Optional[str], optional): The name of the tool to base content-based recommendations on.
                If provided, content-based filtering is utilized.
            num_recommendations (int, optional): The number of recommendations to generate.
                Defaults to 5.

        Returns:
            List[Dict]: A list of recommended tools based on the input parameters.

        Raises:
            ValueError: If num_recommendations is less than 1.
            ValueError: If neither user_id nor tool_name is provided.
        """
        if num_recommendations < 1:
            raise ValueError("num_recommendations must be at least 1.")
        if user_id is None and tool_name is None:
            raise ValueError("At least one of user_id or tool_name must be provided for recommendations.")

        # Determine the recommendation strategy based on provided parameters
        if tool_name:
            recommendations = self.recommend_similar_tools(
                tool_name=tool_name,
                num_recommendations=num_recommendations
            )
        else:
            # If only user_id is provided, this content-based recommender does not handle it
            # It can return an empty list or raise an exception based on design choice
            # Here, we choose to return an empty list
            recommendations = []

        return [tool.__dict__ for tool in recommendations]

    def get_recommendation_scores(self, identifier: str) -> Dict[int, float]:
        """
        Retrieve recommendation scores based on a tool name.
        Since this is a content-based recommender, it does not utilize user_id.

        Args:
            identifier (str): The name of the tool to base scores on.

        Returns:
            Dict[int, float]: A dictionary mapping tool IDs to their corresponding similarity scores.

        Raises:
            ValueError: If the tool_name is not found in the dataset.
        """
        tool_name_lower = identifier.lower()
        if tool_name_lower not in self.tool_names:
            raise ValueError(f"Tool '{identifier}' not found in the dataset.")

        # Find the Tool object
        selected_tool = next(
            (tool for tool in self.tools if tool.name.lower() == tool_name_lower), None
        )

        if not selected_tool:
            raise ValueError(
                f"Tool '{identifier}' not found after initial check."
            )

        # Find the index of the tool in the DataFrame
        tool_index = self.tools_df[self.tools_df['name'].str.lower() == tool_name_lower].index[0]

        if self.similarity_matrix is None:
            return {}

        # Get the similarity scores for the tool
        similarity_scores = list(enumerate(self.similarity_matrix[tool_index]))

        # Create a dictionary of tool_id and their corresponding similarity score
        scores = {
            self.tools_df.iloc[tool[0]]['tool_id']: round(tool[1], 3)
            for tool in similarity_scores if tool[0] != tool_index
        }

        return scores

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
                f"- {tool['name']} - {tool['description']} "
                f"(Category: {tool['category']}, Cost: ${tool['cost']})"
            )

    def recommend_similar_tools(self, tool_name: str, num_recommendations: int = 5) -> List[Tool]:
        """
        Recommends similar tools based on the input tool name.

        Args:
            tool_name (str): The name of the tool to find recommendations for.
            num_recommendations (int, optional): The number of recommendations to return. Defaults to 5.

        Returns:
            List[Tool]: A list of recommended Tool objects.

        Raises:
            ValueError: If the tool_name is not found in the dataset.
        """
        tool_name_lower = tool_name.lower()
        if tool_name_lower not in self.tool_names:
            raise ValueError(f"Tool '{tool_name}' not found in the dataset.")

        # Find the Tool object
        selected_tool = next(
            (tool for tool in self.tools if tool.name.lower() == tool_name_lower), None
        )

        if not selected_tool:
            raise ValueError(
                f"Tool '{tool_name}' not found after initial check."
            )

        # Get recommended Tool objects from the graph
        recommended_tools = self.graph.find_most_relevant_tools(
            start_tool=selected_tool,
            num_recommendations=num_recommendations
        )

        return recommended_tools

    def __repr__(self) -> str:
        """
        Returns a string representation of the ContentBasedRecommender.

        Returns:
            str: String representation.
        """
        return (
            f"ContentBasedRecommender(tools={len(self.tools)}, "
            f"graph={repr(self.graph)}, tree={repr(self.tree)})"
        )
