import json
import csv
from tool import Tool


def load_tools_from_json(file_path):
    """
    Loads tools from a JSON file.

    Args:
        file_path (str): The path to the JSON file containing tool data.

    Returns:
        list: A list of Tool instances.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        tools_data = json.load(file)

    tools = []
    for tool_data in tools_data:
        tool = Tool(
            name=tool_data['name'],
            category=tool_data['category'],
            features=tool_data['features'],
            cost=tool_data['cost'],
            description=tool_data.get('description'),
            url=tool_data.get('url')
        )
        tools.append(tool)

    return tools


def load_tools_from_csv(file_path):
    """
    Loads tools from a CSV file.

    Args:
        file_path (str): The path to the CSV file containing tool data.

    Returns:
        list: A list of Tool instances.
    """

    tools = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tool = Tool(
                name=row['name'],
                category=row['category'],
                # Assuming features are semicolon-separated
                features=row['features'].split(';'),
                cost=float(row['cost']),
                description=row.get('description'),
                url=row.get('url')
            )
            tools.append(tool)

    return tools
