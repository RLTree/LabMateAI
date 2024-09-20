
# LabMate API Documentation

This document provides an overview of the core classes, methods, and functions used in the **LabMate** scientific tool recommendation system. Developers can use this API documentation to understand how to extend and interact with LabMate's internal components.

---

## Table of Contents

1. [Graph Class](#graph-class)
2. [Tree Class](#tree-class)
3. [Recommender Class](#recommender-class)
4. [RequestQueue Class](#requestqueue-class)
5. [CLI Class](#cli-class)
6. [LabMateCore Class](#labmatecore-class)

---

## Graph Class

The `Graph` class manages the relationships between scientific tools, allowing LabMate to suggest similar tools. The graph is built from nodes representing tools and edges representing relationships between them.

### Methods

#### `add_node(tool)`
- **Description**: Adds a node to the graph for a given tool.
- **Arguments**:
  - `tool` (Tool): The tool to be added as a node.

#### `add_edge(tool1, tool2, weight)`
- **Description**: Adds an edge between two tools to indicate their similarity.
- **Arguments**:
  - `tool1` (Tool): The first tool.
  - `tool2` (Tool): The second tool.
  - `weight` (float): The weight of the relationship.

#### `get_neighbors(tool)`
- **Description**: Returns a list of tools connected to the specified tool.
- **Arguments**:
  - `tool` (Tool): The tool whose neighbors you want to retrieve.

#### `find_most_relevant_tools(tool, num_recommendations=5)`
- **Description**: Finds and returns the most relevant tools connected to the specified tool.
- **Arguments**:
  - `tool` (Tool): The starting tool.
  - `num_recommendations` (int, optional): The number of tools to return (default is 5).

---

## Tree Class

The `Tree` class represents the hierarchical structure for categorizing tools. Tools are organized into categories, and each category contains a list of tools.

### Methods

#### `add_tool(tool)`
- **Description**: Adds a tool to the tree under the appropriate category.
- **Arguments**:
  - `tool` (Tool): The tool to be added.

#### `find_category_node(category_name)`
- **Description**: Finds and returns the node representing the specified category.
- **Arguments**:
  - `category_name` (str): The name of the category.

#### `get_tools_in_category(category_name)`
- **Description**: Returns a list of tools in the specified category.
- **Arguments**:
  - `category_name` (str): The category name to retrieve tools from.

#### `search_tools(keyword)`
- **Description**: Searches for tools that match the provided keyword.
- **Arguments**:
  - `keyword` (str): The keyword to search for.

---

## Recommender Class

The `Recommender` class handles the logic for recommending tools based on user input. It interacts with both the `Graph` and `Tree` structures to provide relevant recommendations.

### Methods

#### `build_recommendation_system()`
- **Description**: Builds both the graph and tree structures from the list of tools.

#### `recommend_similar_tools(tool_name, num_recommendations=5)`
- **Description**: Recommends tools that are similar to the specified tool.
- **Arguments**:
  - `tool_name` (str): The name of the tool.
  - `num_recommendations` (int, optional): The number of recommendations to return (default is 5).

#### `recommend_tools_in_category(category_name)`
- **Description**: Recommends tools that belong to a specific category.
- **Arguments**:
  - `category_name` (str): The category name.

#### `search_and_recommend(keyword)`
- **Description**: Searches for tools using the provided keyword and returns recommendations.
- **Arguments**:
  - `keyword` (str): The keyword to search for.

---

## RequestQueue Class

The `RequestQueue` class manages the queue of user requests. It ensures that requests are handled in the order they are received.

### Methods

#### `add_request(request)`
- **Description**: Adds a request to the queue.
- **Arguments**:
  - `request` (dict): A dictionary containing the request details.

#### `process_next()`
- **Description**: Processes the next request in the queue.

#### `is_empty()`
- **Description**: Checks if the queue is empty.
- **Returns**: `True` if the queue is empty, otherwise `False`.

---

## CLI Class

The `CLI` class handles the command-line interface for LabMate. It allows users to input commands and receive tool recommendations.

### Methods

#### `start()`
- **Description**: Starts the CLI and listens for user input.

#### `handle_recommendation(args)`
- **Description**: Handles recommendation requests based on the parsed command-line arguments.

---

## LabMateCore Class

The `LabMateCore` class is the central orchestrator for the system. It coordinates between the CLI, queue, and recommender to process user requests.

### Methods

#### `run()`
- **Description**: Runs the core logic of LabMate, including starting the CLI and processing the request queue.

#### `add_request_to_queue(request)`
- **Description**: Adds a new recommendation request to the queue.
- **Arguments**:
  - `request` (dict): A dictionary containing the recommendation request.

#### `process_queue()`
- **Description**: Processes all requests in the queue.

---

This API documentation covers the main internal components of the **LabMate** system. Developers can use this as a reference to extend or integrate LabMate with other systems.
