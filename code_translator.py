import json
import pandas as pd
from typing import Any, Union

def flatten_json(y: Any) -> dict:
    """
    Recursively flattens a nested JSON dictionary.

    Args:
        y (Any): A dictionary representing the JSON structure.

    Returns:
        dict: A flattened dictionary where nested keys are concatenated with dots.
    """
    out = {}

    def flatten(x: Any, name: str = ''):
        if isinstance(x, dict):
            for key in x:
                flatten(x[key], name + key + '.')
        elif isinstance(x, list):
            for i, item in enumerate(x):
                flatten(item, name + str(i) + '.')
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def load_hierarchical_json(content: Union[str, bytes]) -> pd.DataFrame:
    """
    Loads a hierarchical JSON file of unknown structure into a DataFrame by flattening it.

    Args:
        content (Union[str, bytes]): The content of the JSON file as a string or bytes.

    Returns:
        pd.DataFrame: A DataFrame representing the flattened JSON content.
    """
    # Load JSON content
    if isinstance(content, bytes):
        json_data = json.loads(content.decode('utf-8'))
    else:
        json_data = json.loads(content)
    
    # Check if JSON data is a list or a dictionary
    if isinstance(json_data, dict):
        json_data = [json_data]  # Convert to list for consistent processing

    # Flatten each item in the list (each root-level object) and create a DataFrame
    flattened_data = [flatten_json(item) for item in json_data]
    df = pd.DataFrame(flattened_data)

    return df
