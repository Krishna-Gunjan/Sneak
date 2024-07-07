import json

def read_json(file_path):

    try:
        with open(file_path, 'r') as file:
            return json.load(file)
        
    except FileNotFoundError:
        print(f"File not found: {file_path}")

        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
