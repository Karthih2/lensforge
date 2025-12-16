import json
from backend.llm.client import client
from backend.utils.extract_first_json import extract_first_json

MODEL = "llama-3.1-8b-instant"
TEMPERATURE = 0.0


def scope_agent(topic: str) -> dict:
    prompt = f"""
You are an expert educational content creator.

Rules:
- Output VALID JSON only
- Do not include explanations, comments, or extra text
- Follow the schema exactly

Schema:
{{
  "topic": "string",
  "scope": {{
    "included": ["string"],
    "excluded": ["string"],
    "audience": "string",
    "constraints": ["string"],
    "assumptions": ["string"],
    "prerequisites": ["string"]
  }}
}}

Topic:
{json.dumps(topic)}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a JSON generation engine. Output JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=TEMPERATURE,
        max_tokens=2000
    )

    raw_output = response.choices[0].message.content
    json_text = extract_first_json(raw_output)

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            "Scope Agent returned invalid JSON.\n"
            f"RAW OUTPUT:\n{raw_output}"
        ) from e

