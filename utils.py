import json

def load_data(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
def save_data(users, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)
