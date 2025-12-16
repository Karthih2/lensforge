import json
from backend.llm.client import client
from backend.utils.extract_first_json import extract_first_json

MODEL = "llama-3.1-8b-instant"
TEMPERATURE = 0.0


def roadmap_agent(concepts_output: dict, debates_output: dict) -> dict:
    prompt = f"""
You are an expert curriculum designer.

Rules:
- Output VALID JSON only
- No explanations or text outside JSON
- Follow the schema exactly
- Roadmap must be beginner-friendly
- Progress from fundamentals → applications
- Use concepts and debates to guide ordering

Schema:
{{
  "phases": [
    {{
      "duration": "string",
      "focus": ["string"],
      "outcomes": ["string"],
      "resources": ["string"],
      "success_criteria": ["string"]
    }}
  ]
}}

Concepts:
{json.dumps(concepts_output)}

Debates:
{json.dumps(debates_output)}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a curriculum planning engine. Output JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=TEMPERATURE,
        max_tokens=2000
    )

    raw = response.choices[0].message.content
    json_text = extract_first_json(raw)

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            "Roadmap Agent returned invalid JSON.\n"
            f"RAW OUTPUT:\n{raw}"
        ) from e