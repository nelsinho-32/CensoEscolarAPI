import json


def read(fileName):
    try:
        with open(fileName, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: '{fileName}' file was not found.")
        return []


def write(fileName, data):
    try:
        with open(fileName, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error: {str(e)}")
