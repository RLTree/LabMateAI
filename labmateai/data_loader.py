# labmateai/data_loader.py

"""
This module contains functions for loading tool data from JSON and CSV files.
It ensures that each Tool instance includes a unique tool_id and handles data validation.
"""

import json
import csv
import importlib.resources
from .tool import Tool
import os


def load_tools_from_json(json_filename='tools.json'):
    """
    Loads tools from a JSON file.

    Args:
        json_filename (str): The name of the JSON file containing tool data.
                             Defaults to 'tools.json'.

    Returns:
        list: A list of Tool instances.

    Raises:
        FileNotFoundError: If the JSON file is not found.
        KeyError: If required fields are missing in the JSON data.
        ValueError: If tool_id is missing or not an integer.
    """
    tools = []
    try:
        with importlib.resources.open_text('labmateai.data', json_filename) as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"JSON file '{json_filename}' not found in 'labmateai/data/' directory.")
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Error decoding JSON file '{json_filename}': {str(e)}")

    for index, item in enumerate(data, start=1):
        try:
            tool_id = item['tool_id']
            if not isinstance(tool_id, int):
                raise ValueError(
                    f"tool_id must be an integer in item {index}.")
        except KeyError:
            # Assign a unique tool_id if missing
            tool_id = index
            print(
                f"Warning: 'tool_id' missing for item {index}. Assigning tool_id={tool_id}.")

        try:
            name = item['name'].strip()
            category = item['category'].strip()
            features = [feature.strip().lower()
                        for feature in item.get('features', []) if feature.strip()]
            cost = str(item['cost'])
            description = item['description'].strip()
            url = item['url'].strip()
            language = item['language'].strip()
            platform = item['platform'].strip()
        except KeyError as ke:
            raise KeyError(
                f"Missing required field {ke} in JSON item {index}.")
        except ValueError as ve:
            raise ValueError(
                f"Invalid data format in JSON item {index}: {str(ve)}")

        tool = Tool(
            tool_id=tool_id,
            name=name,
            category=category,
            features=features,
            cost=cost,
            description=description,
            url=url,
            language=language,
            platform=platform
        )
        tools.append(tool)

    return tools


def load_tools_from_csv(csv_filename='tools.csv'):
    """
    Loads tools from a CSV file.

    Args:
        csv_filename (str): The name of the CSV file containing tool data.
                            Defaults to 'tools.csv'.

    Returns:
        list: A list of Tool instances.

    Raises:
        FileNotFoundError: If the CSV file is not found.
        KeyError: If required fields are missing in the CSV data.
        ValueError: If tool_id is missing or not an integer.
    """
    tools = []
    required_fields = ['tool_id', 'name', 'category', 'features',
                       'cost', 'description', 'url', 'platform', 'language']
    csv_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'data', csv_filename)

    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"CSV file '{csv_filename}' not found in 'labmateai/data/' directory.")

    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Check for missing required fields in headers
        missing_fields = [
            field for field in required_fields if field not in reader.fieldnames]
        if missing_fields:
            raise KeyError(
                f"CSV file '{csv_filename}' is missing required fields: {', '.join(missing_fields)}.")

        # start=2 to account for header
        for row_num, row in enumerate(reader, start=2):
            try:
                tool_id = int(row['tool_id'])
            except ValueError:
                raise ValueError(
                    f"Invalid 'tool_id' at row {row_num}. Must be an integer.")

            try:
                name = row['name'].strip()
                category = row['category'].strip()
                features = [feature.strip().lower()
                            for feature in row['features'].split(';') if feature.strip()]
                cost = str(row['cost'])
                description = row['description'].strip()
                url = row['url'].strip()
                language = row['language'].strip()
                platform = row['platform'].strip()
            except KeyError as ke:
                raise KeyError(
                    f"Missing required field {ke} at row {row_num} in CSV.")
            except ValueError as ve:
                raise ValueError(
                    f"Invalid data format at row {row_num} in CSV: {str(ve)}")

            tool = Tool(
                tool_id=tool_id,
                name=name,
                category=category,
                features=features,
                cost=cost,
                description=description,
                url=url,
                language=language,
                platform=platform
            )
            tools.append(tool)

    return tools
