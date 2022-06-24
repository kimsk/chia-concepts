import json

def print_json(dict):
    print(json.dumps(dict, sort_keys=True, indent=4))
