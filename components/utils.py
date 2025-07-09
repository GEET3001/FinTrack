import json
import os
def load_json(filepath):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        return []


def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
