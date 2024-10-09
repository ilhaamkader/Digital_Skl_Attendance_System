import json
from datetime import datetime

class JSONTimestampManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_timestamps(self):
        """Reads the timestamp data from the JSON file."""
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def write_timestamps(self, data):
        """Writes the timestamp data to the JSON file."""
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def update_timestamp(self, class_id):
        """Updates the timestamp for a specific class."""
        data = self.read_timestamps()
        data[class_id] = datetime.now().isoformat()  # Store current time as ISO string
        self.write_timestamps(data)

    def reset_timestamps(self):
        """Resets the JSON file at the end of the day."""
        self.write_timestamps({})
