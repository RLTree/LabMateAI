# recommender.py

"""
Recommender module for suggesting tools based on user input.

This module integrates both content-based and collaborative filtering
recommendation systems to provide comprehensive tool suggestions
within LabMateAI.

Classes:
    Recommender: Handles content-based recommendations using Graph and ToolTree.
"""

import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from .graph import Graph
from .tree import ToolTree
from .tool import Tool
from .collaborative_recommender import CollaborativeRecommender


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


def build_user_item_matrix(interactions):
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


class Recommender:
    """
    Handles content-based recommendations using Graph and ToolTree.
    """

    def __init__(self, tools):
        """
        Initializes the Recommender with a list of tools.

        Args:
            tools (list): A list of Tool objects to be used for recommendations.
        """
        # Check for duplicate tool IDs
        tool_ids = set()
        for tool in tools:
            if tool.tool_id in tool_ids:
                raise ValueError(
                    f"Tool '{tool.name}' already exists in the graph.")
            tool_ids.add(tool.tool_id)

        self.graph = Graph(tools)
        self.tree = ToolTree()
        self.tools = tools
        self.tool_names = {tool.name.lower()
                           for tool in tools}  # For case-insensitive matching
        self.build_recommendation_system()

        # Preprocess tools for content-based filtering
        self.tools_df = pd.DataFrame([tool.__dict__ for tool in tools])
        self.tools_df['combined_features'] = self.tools_df.apply(
            lambda row: self._combine_features(row), axis=1
        )
        self.vectorizer = CountVectorizer().fit_transform(
            self.tools_df['combined_features'])
        self.similarity_matrix = cosine_similarity(self.vectorizer)

    def _combine_features(self, row):
        """
        Combine selected features into a single string for each tool.

        Args:
            row (pd.Series): A row from the tools DataFrame.

        Returns:
            str: A string combining the features for content-based similarity calculations.
        """
        return f"{row['name']} {row['category']} {' '.join(row['features'])} {row['language']} {row['platform']}"

    def build_recommendation_system(self):
        """
        Builds the recommendation system by constructing the graph and tree.
        """
        self.graph.build_graph(self.tools)
        self.tree.build_tree(self.tools)

    def recommend_similar_tools(self, tool_name, num_recommendations=5):
        """
        Recommends similar tools based on the input tool name.

        Args:
            tool_name (str): The name of the tool to find recommendations for.
            num_recommendations (int): The number of recommendations to return.

        Returns:
            list: A list of recommended Tool objects.

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
                f"Tool '{tool_name}' not found after initial check.")

        # Get recommended Tool objects from the graph
        recommended_tools = self.graph.find_most_relevant_tools(
            start_tool=selected_tool,
            num_recommendations=num_recommendations
        )

        return recommended_tools

    def recommend_tools_in_category(self, category_name):
        """
        Recommends tools based on the specified category.

        Args:
            category_name (str): The name of the category to find recommendations for.

        Returns:
            list: A list of recommended Tool objects in the specified category.

        Raises:
            ValueError: If the category_name is not found in the dataset.
        """
        try:
            recommendations = self.tree.get_tools_in_category(category_name)
            return recommendations
        except ValueError as e:
            raise ValueError(str(e)) from e

    def search_and_recommend(self, keyword):
        """
        Searches for tools based on a keyword and recommends them.

        Args:
            keyword (str): The keyword to search for.

        Returns:
            list: A list of recommended Tool objects based on the search.
        """
        recommendations = self.tree.search_tools(keyword)
        return recommendations

    def recommend(self, tool_name=None, category_name=None, keyword=None, num_recommendations=5):
        """
        Provides recommendations based on the input parameters.

        Args:
            tool_name (str, optional): The name of the tool to find recommendations for.
            category_name (str, optional): The name of the category to find recommendations for.
            keyword (str, optional): The keyword to search for.
            num_recommendations (int, optional): The number of recommendations to generate.

        Returns:
            list: A list of recommended Tool objects based on the input parameters.
        """
        if tool_name:
            recommendations = self.recommend_similar_tools(
                tool_name=tool_name,
                num_recommendations=num_recommendations
            )
        elif category_name:
            recommendations = self.recommend_tools_in_category(category_name)
        elif keyword:
            recommendations = self.search_and_recommend(keyword)
        else:
            raise ValueError(
                "At least one of tool_name, category_name, or keyword must be provided.")

        return recommendations

    def get_recommendation_scores(self, tool_name: str) -> dict:
        """
        Returns content-based recommendation scores for a given tool.

        Args:
            tool_name (str): The name of the tool for which to get recommendations.

        Returns:
            dict: Dictionary where keys are tool_ids and values are similarity scores.
        """
        if tool_name.lower() not in self.tools_df['name'].str.lower().values:
            raise ValueError(f"Tool '{tool_name}' not found in the dataset.")

        tool_index = self.tools_df[self.tools_df['name'].str.lower(
        ) == tool_name.lower()].index[0]

        # Get the similarity scores for the tool
        similarity_scores = list(enumerate(self.similarity_matrix[tool_index]))

        # Create a dictionary of tool_id and their corresponding similarity score
        scores = {
            self.tools_df.iloc[tool[0]]['tool_id']: round(tool[1], 3)
            for tool in similarity_scores if tool[0] != tool_index
        }

        return scores

    def display_recommendations(self, recommendations):
        """
        Displays the recommended tools.

        Args:
            recommendations (list): A list of recommended Tool objects to display.
        """
        print("\nRecommended Tools:")
        if not recommendations:
            print("No recommendations found.")
        else:
            for tool in recommendations:
                print(
                    f"- {tool.name} - {tool.description} "
                    f"(Category: {tool.category}, Cost: ${tool.cost})"
                )


def main():
    """
    Main function to demonstrate content-based and collaborative filtering recommendations.
    """
    # Load data
    users, tools_df, interactions = load_data()
    user_item_matrix = build_user_item_matrix(interactions)

    # Convert tools_df to a list of Tool objects
    tools = [
        Tool(
            tool_id=int(row['tool_id']),
            name=row['name'],
            category=row['category'],
            features=[feature.strip().lower()
                      for feature in row['features'].split(';') if feature.strip()],
            cost=str(row['cost']),
            description=row['description'],
            url=row['url'],
            language=row['language'],
            platform=row['platform']
        )
        for _, row in tools_df.iterrows()
    ]

    # Initialize the Recommender for content-based recommendations
    recommender = Recommender(tools)

    # Content-Based Recommendation Example
    content_tool_name = "ToolA"  # Example tool name
    try:
        content_recommendations = recommender.recommend(
            tool_name=content_tool_name,
            num_recommendations=5
        )
        print(f"\nContent-Based Recommendations for '{content_tool_name}':")
        recommender.display_recommendations(content_recommendations)
    except ValueError as e:
        print(e)

    # Initialize Collaborative Filtering Recommender
    cf_recommender = CollaborativeRecommender(
        user_item_matrix, tools_df, n_neighbors=5)

    # Collaborative Filtering Recommendation Example
    user_id = 1  # Example user ID
    try:
        cf_recommendations = cf_recommender.get_recommendations(
            user_id=user_id,
            n_recommendations=5
        )
        print(f"\nCollaborative Filtering Recommendations for User {user_id}:")
        for tool in cf_recommendations:
            print(f"- {tool['tool_name']} (ID: {tool['tool_id']})")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
