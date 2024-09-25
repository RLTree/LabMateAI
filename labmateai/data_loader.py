# labmateai/data_loader.py

"""
This module contains functions for loading tool data from JSON and CSV files.
"""

import json
import csv
import importlib.resources
from .tool import Tool


def load_tools_from_json():
    """
    Loads tools from a JSON file.

    Returns:
        list: A list of Tool instances.
    """

    with importlib.resources.open_text('labmateai.data', 'tools.json') as file:
        data = json.load(file)
    tools = []
    for item in data:
        # Access required fields directly to ensure KeyError is raised if missing
        tool = Tool(
            name=item['name'],
            category=item['category'],
            features=item.get('features', []),
            cost=item['cost'],
            description=item['description'],
            url=item['url'],
            platform=item['platform'],
            language=item['language']
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
    required_fields = ['name', 'category', 'features',
                       'cost', 'description', 'url', 'platform', 'language']
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Check if CSV has headers
        if reader.fieldnames is None:
            raise KeyError("CSV file is missing header.")

        # Check for missing required fields in headers
        missing_fields = [
            field for field in required_fields if field not in reader.fieldnames]
        if missing_fields:
            raise KeyError(
                f"CSV file is missing required fields: {', '.join(missing_fields)}.")

        # start=2 to account for header
        for row_num, row in enumerate(reader, start=2):
            # Validate presence and non-emptiness of required fields
            for field in required_fields:
                value = row.get(field)
                if value is None or not value.strip():
                    raise KeyError(
                        f"Missing or empty required field '{field}' in row {row_num}.")

            # Create Tool instance
            tool = Tool(
                name=row['name'],
                category=row['category'],
                # Assuming features are semicolon-separated; handle empty features gracefully
                features=row['features'].split(
                    ';') if row['features'].strip() else [],
                cost=row['cost'],
                description=row['description'],
                url=row['url'],
                platform=row['platform'],
                language=row['language']
            )
            tools.append(tool)

    return tools
