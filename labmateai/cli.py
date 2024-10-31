# labmateai/cli.py

"""
CLI module for LabMateAI.

This module provides the CLI class, which handles user interactions
and provides tool recommendations based on user input.
"""

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv
from importlib import resources
from alembic import command
from alembic.config import Config
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
load_dotenv()


class CLI:
    """
    Command-Line Interface for LabMateAI.
    """

    def __init__(self, testing=False):
        """
        Initializes the CLI and ensures the database is initialized.

        Args:
            testing (bool): If True, uses a test database configuration.
        """
        self.testing = testing
        self.db_config = {
            'dbname': os.getenv('DB_NAME', 'de66dcp38h2o4m'),
            'user': os.getenv('DB_USER', 'u57kmcm3orlrse'),
            'password': os.getenv('DB_PASSWORD', 'p9ba3c40033c848824b46a92c562a41564a01454a9de36d46c8435d518715185f'),
            'host': os.getenv('DB_HOST', 'c1v04v8krpfbct.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com'),
            'port': os.getenv('DB_PORT', '5432')
        }
        self.tools = None
        self.recommender = None
        self.cf_recommender = None
        self.hybrid_recommender = None
        self.data_loaded = False

        # Initialize the database migrations
        if not self.testing:
            self._run_migrations()
        else:
            logging.info("Skipping migrations during testing.")

        # Initialize the database engine and session
        self.engine = self._get_engine()
        self.Session = self._get_session_maker()

    def _get_engine(self):
        """
        Lazily imports and returns the SQLAlchemy engine.
        """
        from .labmateai_db import get_engine
        if self.testing:
            os.environ['TESTING'] = 'True'
        return get_engine(self.db_config)

    def _get_session_maker(self):
        """
        Creates and returns a sessionmaker bound to the engine.
        """
        from sqlalchemy.orm import sessionmaker
        return sessionmaker(bind=self.engine)

    def _run_migrations(self):
        """
        Runs Alembic migrations to ensure the database schema is up-to-date.
        """
        if self.testing:
            # Skip migrations during testing
            logging.info("Skipping migrations during testing.")
            return

        try:
            # Locate alembic.ini within the labmateai package
            with resources.path('labmateai', 'alembic.ini') as alembic_ini_path:
                logging.debug(f"Looking for alembic.ini at: {alembic_ini_path}")
                if not alembic_ini_path.exists():
                    raise FileNotFoundError(f"alembic.ini not found at {alembic_ini_path}")
                alembic_cfg = Config(str(alembic_ini_path))
            
                # Set the sqlalchemy.url in Alembic configuration to the DATABASE_URL
                alembic_cfg.set_main_option('sqlalchemy.url', self._construct_database_url())

                # Run migrations
                logging.info("Running Alembic migrations...")
                command.upgrade(alembic_cfg, "head")
                logging.info("Alembic migrations applied successfully.")
        except Exception as e:
            logging.error("Failed to apply Alembic migrations: %s", e)
            print("Migration failed. Please check the logs for more details.")
            sys.exit(1)

    def _construct_database_url(self):
        """
        Constructs the DATABASE_URL from individual components.

        Returns:
            str: The constructed DATABASE_URL.
        """
        if os.getenv('TESTING') == 'True':
            return 'sqlite:///:memory:'
        return f"postgresql://{self.db_config['user']}:{self.db_config['password']}@" \
               f"{self.db_config['host']}:{self.db_config['port']}/{self.db_config['dbname']}"

    def _get_or_create_user(self):
        """
        Handles user login or sign-up.
        """
        # Import models and sessionmaker here to avoid module-level imports
        from .models import User

        session = self.Session()
        try:
            print("\n--- LabMateAI User Login/Signup ---")
            email = input("Enter your email: ").strip().lower()

            user = session.query(User).filter_by(email=email).first()

            if user:
                print(f"Welcome back, {user.user_name}.")
                user_id = user.user_id
            else:
                print("No account found. Let's create a new one.")
                user_name = input("Enter your full name: ").strip()
                department = input("Enter your department: ").strip()
                role = input(
                    "Enter your role (e.g., Researcher, Student): ").strip()

                new_user = User(
                    user_name=user_name,
                    email=email,
                    department=department,
                    role=role
                )
                session.add(new_user)
                session.commit()
                session.refresh(new_user)  # Refresh to get the user_id
                print(
                    f"User successfully signed up! Welcome, {new_user.user_name}.")
                user_id = new_user.user_id

            return user_id
        except Exception as e:
            logging.error("Database error during user login/signup: %s", e)
            print("An error occurred during login/signup. Please try again.")
            sys.exit(1)
        finally:
            session.close()

    def _log_interaction(self, user_id, tool_id, rating=None, usage_frequency=None):
        """
        Logs an interaction into the interactions table.

        Args:
            user_id (int): The ID of the user.
            tool_id (int): The ID of the tool.
            rating (int, optional): User rating for the tool (0-5).
            usage_frequency (str, optional): Frequency of tool usage.
        """
        # Import models here to avoid module-level imports
        from .models import Interaction

        session = self.Session()
        try:
            interaction = Interaction(
                user_id=user_id,
                tool_id=tool_id,
                rating=rating,
                usage_frequency=usage_frequency,
                timestamp=datetime.now()
            )
            session.add(interaction)
            session.commit()
            print("Thank you for your interaction!")
        except Exception as e:
            logging.error("Failed to log interaction: %s", e)
            print("An error occurred while logging your interaction. Please try again.")
        finally:
            session.close()

    def _get_number_of_recommendations(self):
        """
        Prompts the user to enter the number of recommendations they want.
        Defaults to 3 if no valid input is provided.

        Returns:
            int: Number of recommendations.
        """
        while True:
            num_input = input("How many recommendations would you like? (default 3): ").strip()
            if num_input == '':
                return 3
            elif num_input.isdigit() and int(num_input) > 0:
                return int(num_input)
            else:
                print("Please enter a positive integer.")

    def _load_data_and_initialize_recommenders(self):
        """
        Loads data and initializes the recommenders.
        """
        if not self.data_loaded:
            try:
                # Import models and recommender classes here
                from .models import Tool as ToolModel, Interaction
                from .recommenders.content_based_recommender import ContentBasedRecommender, build_user_item_matrix
                from .recommenders.collaborative_recommender import CollaborativeRecommender
                from .recommenders.hybrid_recommender import HybridRecommender
                from .tool import Tool as CustomTool

                session = self.Session()

                # Load tools from the tools table
                tools_data = session.query(ToolModel).all()
                if not tools_data:
                    raise RuntimeError("No tools found in the database.")

                self.tools = []
                for tool in tools_data:
                    # Debugging: Check the type and content of tool.features
                    logging.debug(
                        f"Tool ID: {tool.tool_id}, Features: {tool.features}, Type: {type(tool.features)}")

                    if isinstance(tool.features, list):
                        # features is already a list
                        features_processed = [feature.strip().lower()
                                              for feature in tool.features if feature.strip()]
                    elif isinstance(tool.features, str):
                        # Assuming features are stored as "{feature1, feature2, feature3}"
                        # Remove curly braces and split by comma
                        features_cleaned = tool.features.strip('{}')
                        features_split = [
                            feature.strip() for feature in features_cleaned.split(',') if feature.strip()]
                        features_processed = [feature.lower()
                                              for feature in features_split]
                    else:
                        logging.warning(
                            f"Unexpected type for features in tool ID {tool.tool_id}. Skipping this tool.")
                        continue  # Skip this tool if features are not in expected format

                    custom_tool = CustomTool(
                        tool_id=tool.tool_id,
                        name=tool.name,
                        category=tool.category,
                        features=tuple(features_processed),
                        cost=tool.cost,
                        description=tool.description,
                        url=tool.url,
                        language=tool.language,
                        platform=tool.platform
                    )
                    self.tools.append(custom_tool)

                # Initialize the Recommender for content-based recommendations
                self.recommender = ContentBasedRecommender(tools=self.tools)

                # Load user-item interactions from the database
                interactions_data = session.query(Interaction).filter(
                    Interaction.rating.isnot(None)).all()

                if interactions_data:
                    interactions = pd.DataFrame([{
                        'user_id': interaction.user_id,
                        'tool_id': interaction.tool_id,
                        'rating': interaction.rating
                    } for interaction in interactions_data])

                    logging.debug("Interactions DataFrame: \n%s", interactions)

                    # Build user-item matrix
                    if not interactions.empty:
                        user_item_matrix = build_user_item_matrix(interactions)
                        logging.debug("User-item matrix: \n%s", user_item_matrix)

                        # Initialize Collaborative Filtering Recommender
                        if not user_item_matrix.empty:
                            tools_df = pd.DataFrame([{
                                'tool_id': tool.tool_id,
                                'name': tool.name,
                                'category': tool.category,
                                'features': tool.features,
                                'cost': tool.cost,
                                'description': tool.description,
                                'url': tool.url,
                                'language': tool.language,
                                'platform': tool.platform
                            } for tool in tools_data])

                            self.cf_recommender = CollaborativeRecommender(
                                user_item_matrix=user_item_matrix,
                                tools_df=tools_df,
                                n_neighbors=5
                            )

                            # Initialize Hybrid Recommender
                            self.hybrid_recommender = HybridRecommender(
                                content_recommender=self.recommender,
                                collaborative_recommender=self.cf_recommender,
                                alpha=0.5
                            )
                        else:
                            logging.warning(
                                "User-item matrix is empty. Collaborative filtering will not be available.")
                            self.cf_recommender = None
                            self.hybrid_recommender = None
                    else:
                        logging.warning(
                            "Interactions DataFrame is empty. Collaborative filtering will not be available.")
                        self.cf_recommender = None
                        self.hybrid_recommender = None
                else:
                    logging.warning("No interactions found in the database.")
                    self.cf_recommender = None
                    self.hybrid_recommender = None

                # Mark data as loaded
                self.data_loaded = True

                # Print loaded tools
                tool_names = [tool.name for tool in self.tools]
                logging.info("Loaded tools: %s", tool_names)

                session.close()

            except Exception as e:
                logging.error("Failed to initialize CLI: %s", e)
                print(
                    "Failed to initialize the application. Please ensure the database is set up correctly.")
                sys.exit(1)

    def _prompt_rating(self, recommendations, user_id):
        """
        Prompts the user to rate any of the recommended tools.

        Args:
            recommendations (list of CustomTool): List of recommended tools.
            user_id (int): The ID of the current user.
        """
        while True:
            rate_choice = input(
                "Would you like to rate any of these tools? (yes/no): ").strip().lower()
            if rate_choice in ['yes', 'y']:
                try:
                    tool_id_input = input(
                        "Enter the Tool ID you want to rate: ").strip()
                    if not tool_id_input.isdigit():
                        print("Invalid Tool ID. Please enter a numeric value: ")
                        continue
                    tool_id = int(tool_id_input)

                    # Checking if tool_id is in recommendations
                    if not any(tool.tool_id == tool_id for tool in recommendations):
                        print("The Tool ID is not in the current recommendations.")
                        continue

                    rating_input = input(
                        "Enter your rating for the tool (0-5): ").strip()
                    while not rating_input.isdigit() or not (0 <= int(rating_input) <= 5):
                        rating_input = input("Invalid rating. Please enter a numeric value between 0 and 5: ").strip()
                    rating = int(rating_input)

                    # Prompt for usage frequency
                    usage_frequency = input(
                        "Enter your usage frequency for the tool (e.g., Often, Sometimes, Rarely, Never): ").strip()

                    # Log the interaction
                    self._log_interaction(
                        user_id=user_id, tool_id=tool_id, rating=rating, usage_frequency=usage_frequency)
                    break
                except ValueError:
                    print(
                        "Invalid input. Please ensure all entries are correct.")
            elif rate_choice in ['no', 'n']:
                break
            else:
                print("Please respond with 'yes' or 'no'.")

    def handle_recommend_similar_tools(self, user_id):
        """
        Handles recommending similar tools based on a tool name provided by the user.
        """
        try:
            tool_name = input("Enter the name of a tool you like: ").strip()
            num_recommendations = self._get_number_of_recommendations()
            recommendations = self.recommender.recommend_similar_tools(tool_name, num_recommendations)
            if recommendations:
                print("\nRecommendations:")
                for tool in recommendations:
                    print(
                        f"- {tool.name} (ID: {tool.tool_id}): {tool.description} (Cost: {tool.cost})")
                # Prompt for rating after recommendations
                self._prompt_rating(recommendations, user_id)
            else:
                print("No similar tools found.")
        except Exception as e:
            logging.error("Error during recommending similar tools: %s", e)
            print("An error occurred while fetching recommendations. Please try again.")

    def handle_recommend_category_tools(self, user_id):
        """
        Handles recommending tools within a specified category.
        """
        try:
            category = input(
                "Enter the category of tools you're interested in: ").strip()
            num_recommendations = self._get_number_of_recommendations()
            recommendations = [
                tool for tool in self.tools if tool.category.lower() == category.lower()]

            # Limit the number of recommendations
            recommendations = recommendations[:num_recommendations]

            if recommendations:
                print("\nRecommendations:")
                for tool in recommendations:
                    print(
                        f"- {tool.name} (ID: {tool.tool_id}): {tool.description} (Cost: {tool.cost})")
                # Prompt for rating after recommendations
                self._prompt_rating(recommendations, user_id)
            else:
                print("No tools found in this category.")
        except Exception as e:
            logging.error("Error during recommending category tools: %s", e)
            print("An error occurred while fetching recommendations. Please try again.")

    def handle_search_tools(self, user_id):
        """
        Handles searching for tools based on a keyword.
        """
        try:
            keyword = input(
                "Enter a keyword to search for tools: ").strip().lower()
            num_recommendations = self._get_number_of_recommendations()
            recommendations = [
                tool for tool in self.tools if keyword in tool.name.lower() or keyword in tool.description.lower()
            ]

            # Limit the number of recommendations
            recommendations = recommendations[:num_recommendations]

            if recommendations:
                print("\nSearch Results:")
                for tool in recommendations:
                    print(
                        f"- {tool.name} (ID: {tool.tool_id}): {tool.description} (Cost: {tool.cost})")
                # Prompt for rating after recommendations
                self._prompt_rating(recommendations, user_id)
            else:
                print("No tools found for the given keyword.")
        except Exception as e:
            logging.error("Error during searching tools: %s", e)
            print("An error occurred while searching for tools. Please try again.")

    def start(self):
        """
        Starts the interactive CLI session.
        """
        user_id = self._get_or_create_user()
        self._load_data_and_initialize_recommenders()

        while True:
            print("\n--- LabMateAI Tool Recommender ---")
            print("Please select an option:")
            print("1. Recommend similar tools")
            print("2. Recommend tools within a category")
            print("3. Search tools by keyword")
            print("4. Exit")

            choice = input("Enter your choice (1-4): ").strip()

            if choice == '1':
                self.handle_recommend_similar_tools(user_id)
            elif choice == '2':
                self.handle_recommend_category_tools(user_id)
            elif choice == '3':
                self.handle_search_tools(user_id)
            elif choice == '4':
                print("Exiting LabMateAI. Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")


def main():
    cli = CLI()
    cli.start()


if __name__ == "__main__":
    main()
