
# LabMateAI API Documentation

This document provides an overview of the core classes, methods, and functions used in the **LabMateAI** scientific tool recommendation system. Developers can use this API documentation to understand how to extend and interact with LabMateAI's internal components.

---

## Table of Contents

1. [Tool Class](#tool-class)
2. [Graph Class](#graph-class)
3. [ToolTree Class](#tooltree-class)
4. [Recommender Class](#recommender-class)
5. [CLI Class](#cli-class)
6. [Data Loader Module](#data-loader-module)

---

## Tool Class

The `Tool` class represents an individual scientific tool with its associated attributes.

### Attributes

- **name** (`str`): The name of the tool.
- **category** (`str`): The category to which the tool belongs.
- **features** (`list` of `str`): A list of features associated with the tool.
- **cost** (`str`): The cost of the tool (e.g., "Free", "Paid").
- **description** (`str`): A brief description of the tool.
- **url** (`str`): The URL to the tool's homepage or repository.
- **language** (`str`, optional): The programming language associated with the tool.
- **platform** (`str`, optional): The platform(s) the tool supports (e.g., "Windows", "macOS", "Linux", "Web-Based").

### Methods

#### `__init__(self, name, category, features, cost, description, url, language=None, platform=None)`

- **Description**: Initializes a new instance of the `Tool` class.
- **Parameters**:
  - `name` (`str`): The name of the tool.
  - `category` (`str`): The category of the tool.
  - `features` (`list` of `str`): Features associated with the tool.
  - `cost` (`str`): The cost of the tool.
  - `description` (`str`): A brief description.
  - `url` (`str`): The URL to the tool's homepage.
  - `language` (`str`, optional): Programming language used.
  - `platform` (`str`, optional): Supported platforms.

---

## Graph Class

The `Graph` class manages the relationships between scientific tools, allowing LabMateAI to suggest similar tools. The graph is built from nodes representing tools and edges representing the similarity between them.

### Methods

#### `build_graph(self, tools)`

- **Description**: Builds the graph by adding nodes and edges based on the list of tools.
- **Parameters**:
  - `tools` (`list` of `Tool`): The list of tools to build the graph from.

#### `add_node(self, tool)`

- **Description**: Adds a node to the graph for a given tool.
- **Parameters**:
  - `tool` (`Tool`): The tool to be added as a node.

#### `add_edge(self, tool1, tool2, weight)`

- **Description**: Adds an edge between two tools to indicate their similarity.
- **Parameters**:
  - `tool1` (`Tool`): The first tool.
  - `tool2` (`Tool`): The second tool.
  - `weight` (`float`): The weight representing dissimilarity (1 - similarity).

#### `get_neighbors(self, tool)`

- **Description**: Returns a list of neighboring tools connected to the specified tool.
- **Parameters**:
  - `tool` (`Tool`): The tool whose neighbors you want to retrieve.
- **Returns**:
  - `neighbors` (`list` of `Tool`): A list of neighboring tools.

---

## ToolTree Class

The `ToolTree` class represents the hierarchical structure for categorizing tools. Tools are organized into categories, and each category contains a list of tools.

### Methods

#### `build_tree(self, tools)`

- **Description**: Builds the tree structure based on the list of tools.
- **Parameters**:
  - `tools` (`list` of `Tool`): The list of tools to build the tree from.

#### `add_tool(self, tool)`

- **Description**: Adds a tool to the tree under the appropriate category.
- **Parameters**:
  - `tool` (`Tool`): The tool to be added.

#### `get_tools_in_category(self, category_name)`

- **Description**: Returns a list of tools in the specified category.
- **Parameters**:
  - `category_name` (`str`): The category name to retrieve tools from.
- **Returns**:
  - `tools` (`list` of `Tool`): A list of tools in the category.

#### `search_tools(self, keyword)`

- **Description**: Searches for tools that match the provided keyword in their name, description, or features.
- **Parameters**:
  - `keyword` (`str`): The keyword to search for.
- **Returns**:
  - `results` (`list` of `Tool`): A list of matching tools.

#### `get_all_categories(self)`

- **Description**: Returns a list of all categories in the tree.
- **Returns**:
  - `categories` (`list` of `str`): A list of category names.

---

## Recommender Class

The `Recommender` class handles the logic for recommending tools based on user input. It interacts with both the `Graph` and `ToolTree` structures to provide relevant recommendations.

### Methods

#### `__init__(self, tools)`

- **Description**: Initializes the Recommender with a list of tools.
- **Parameters**:
  - `tools` (`list` of `Tool`): The list of tools to build the recommendation system from.

#### `build_recommendation_system(self)`

- **Description**: Builds both the graph and tree structures from the list of tools.

#### `recommend_similar_tools(self, tool_name, num_recommendations=5)`

- **Description**: Recommends tools that are similar to the specified tool.
- **Parameters**:
  - `tool_name` (`str`): The name of the tool.
  - `num_recommendations` (`int`, optional): The number of recommendations to return (default is 5).
- **Returns**:
  - `recommendations` (`list` of `Tool`): A list of recommended tools.
- **Raises**:
  - `ValueError`: If the tool is not found.

#### `recommend_tools_in_category(self, category_name)`

- **Description**: Recommends tools that belong to a specific category.
- **Parameters**:
  - `category_name` (`str`): The category name.
- **Returns**:
  - `recommendations` (`list` of `Tool`): A list of tools in the category.
- **Raises**:
  - `ValueError`: If the category is not found.

#### `search_and_recommend(self, keyword)`

- **Description**: Searches for tools using the provided keyword and returns matching tools.
- **Parameters**:
  - `keyword` (`str`): The keyword to search for.
- **Returns**:
  - `results` (`list` of `Tool`): A list of matching tools.

---

## CLI Class

The `CLI` class handles the command-line interface for LabMateAI. It allows users to interactively input commands and receive tool recommendations.

### Methods

#### `__init__(self, tools)`

- **Description**: Initializes the CLI with a list of tools.
- **Parameters**:
  - `tools` (`list` of `Tool`): The list of tools for recommendations.

#### `start(self)`

- **Description**: Starts the CLI and listens for user input, presenting a menu of options.

#### `recommend_similar_tools(self)`

- **Description**: Prompts the user for a tool name and number of recommendations, then displays similar tools.

#### `recommend_tools_in_category(self)`

- **Description**: Prompts the user for a category name and displays tools in that category.

#### `search_tools(self)`

- **Description**: Prompts the user for a keyword and displays matching tools.

---

## Data Loader Module

The `data_loader` module provides functions to load tool data from JSON files or other sources.

### Functions

#### `load_tools_from_json(filepath)`

- **Description**: Loads tool data from a JSON file and returns a list of `Tool` instances.
- **Parameters**:
  - `filepath` (`str`): The path to the JSON file containing tool data.
- **Returns**:
  - `tools` (`list` of `Tool`): A list of tools created from the JSON data.

---

This API documentation covers the main internal components of the **LabMateAI** system. Developers can use this as a reference to extend or integrate LabMateAI with other systems.

---

**Note**: The functionality previously handled by the `RequestQueue` and `LabMateCore` classes has been integrated into other components like the `CLI` and `Recommender` classes to streamline the system.
