import json

def read_theme(file_path):

    # Refer to the comment in src/map_reader.py

    try:
        with open(file_path, 'r') as file:
            theme = json.load(file)
        return {key: tuple(value) for key, value in theme.items()}
    
    except FileNotFoundError:
        raise Exception("Theme file not found")
