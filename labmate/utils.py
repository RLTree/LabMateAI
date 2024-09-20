
import json


def load_tools_from_json(file_path):
    """
    Loads tools from a JSON file.

    Args:
        file_path (str): Path to the JSON file containing tool data.

    Returns:
        list: A list of tool dictionaries.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tools = json.load(file)
        return tools
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode the JSON file {file_path}.")
        return []


def validate_input(input_str):
    """
    Validates user input, ensuring that it is not empty and is of correct format.

    Args:
        input_str (str): The user's input string.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    if not input_str or not isinstance(input_str, str):
        print("Invalid input. Please enter a valid string.")
        return False
    return True


def format_tool_output(tool):
    """
    Formats the tool information for display.

    Args:
        tool (dict): A dictionary representing a tool.

    Returns:
        str: A formatted string representation of the tool.
    """
    return f"{tool['name']} - {tool['description']} (Category: {tool['category']}, Cost: {tool['cost']})"


def search_tools_by_keyword(tools, keyword):
    """
    Searches for tools by a given keyword in their name or description.

    Args:
        tools (list): A list of tool dictionaries.
        keyword (str): The keyword to search for.

    Returns:
        list: A list of tools that match the keyword.
    """
    results = [tool for tool in tools if keyword.lower() in tool['name'].lower(
    ) or keyword.lower() in tool['description'].lower()]
    return results


def sort_tools_by_name(tools):
    """
    Sorts a list of tools alphabetically by their name.

    Args:
        tools (list): A list of tool dictionaries.

    Returns:
        list: The list of tools sorted by name.
    """
    return sorted(tools, key=lambda tool: tool['name'].lower())


def save_results_to_file(results, file_path):
    """
    Saves the recommendation results to a file.

    Args:
        results (list): A list of tool dictionaries representing the recommendation results.
        file_path (str): The path to the file where results should be saved.
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(results, file, indent=4)
        print(f"Results saved to {file_path}.")
    except IOError:
        print(f"Error: Could not write to file {file_path}.")


def display_recommendations(recommendations):
    """
    Displays the formatted recommendations.

    Args:
        recommendations (list): A list of tool dictionaries representing the recommendations.
    """
    if not recommendations:
        print("No recommendations found.")
    else:
        for tool in recommendations:
            print(format_tool_output(tool))
