"""
The core module of the LabMate application, responsible for managing the main functionalities and interactions.
"""

from queue import RequestQueue
from recommender import Recommender
from cli import CLI
from data_loader import load_tools_from_json


class LabMateCore:
    """
    The core class for managing the LabMate application. It integrates the queue, recommender, and CLI to handle user input and provide recommendations.
    """

    def __init__(self, tools):
        """
        Initializes the LabMateCore with a recommender and a request queue.
        """
        tools = load_tools_from_json('tools.json')
        self.tools = tools
        self.recommender = Recommender(tools)
        self.request_queue = RequestQueue()
        self.cli = CLI(tools)

    def run(self):
        """
        Starts the LabMate application.
        """

        self.cli.start()
        self.request_queue.process_next()

    def add_request_to_queue(self, request):
        """
        Adds a recommendation request to the queue.
        """

        self.request_queue.add_request(request)

    def process_queue(self):
        """
        Processes the request queue and provides recommendations based on the requests.
        """

        while not self.request_queue.is_empty():
            current_request = self.request_queue.process_next()
            if current_request['type'] == 'similar':
                results = self.recommender.recommend_similar_tools(
                    current_request['tool_name'])
            elif current_request['type'] == 'category':
                results = self.recommender.recommend_tools_in_category(
                    current_request['category_name'])
            elif current_request['type'] == 'search':
                results = self.recommender.search_and_recommend(
                    current_request['keyword'])

            self.display_results(results)

    def display_results(self, results):
        """
        Displays the results of the recommendations.
        """

        self.recommender.display_recommendations(results)
