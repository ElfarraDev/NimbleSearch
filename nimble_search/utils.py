import json

def load_json(file_path):
    """
    Load a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Loaded JSON data.
    """
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data, file_path):
    """
    Save data to a JSON file.

    Args:
        data (dict): Data to save.
        file_path (str): Path to save the JSON file.
    """
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
