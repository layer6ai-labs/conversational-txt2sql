import json
from models.database import Data
class DataHandler:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def load_data(self):
        """Load data from a jsonl file."""
        try:
            with open(self.input_path, 'r') as file:
                data = [json.loads(line) for line in file]
                return [Data(**item) for item in data]
        except FileNotFoundError:
            print(f"File {self.input_path} not found.")
            return []
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {self.input_path}.")
            return []

    def save_data(self, data):
        """Save data to a JSONL file."""
        try:
            with open(self.output_path, 'w') as file:
                for item in data:
                    file.write(json.dumps(item) + '\n')
        except IOError as e:
            print(f"Error writing to file {self.output_path}: {e}")
