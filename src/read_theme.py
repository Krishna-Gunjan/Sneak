import json

def read_theme(file_path):
    try:
        with open(file_path, 'r') as file:
            theme = json.load(file)
        return {key: tuple(value) for key, value in theme.items()}
    except FileNotFoundError:
        raise Exception("Theme file not found")
