# backend/utils/json_extract.py

def extract_first_json(text: str) -> str:
    depth = 0
    start = None

    for i, char in enumerate(text):
        if char == "{":
            if depth == 0:
                start = i
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0 and start is not None:
                return text[start:i + 1]

    raise ValueError("No complete JSON object found")
