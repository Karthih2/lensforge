import json
from backend.llm.client import client
from backend.utils.extract_first_json import extract_first_json

MODEL = "llama-3.1-8b-instant"
TEMPERATURE = 0.0


def resource_agent(concepts_output: dict, roadmap_output: dict) -> dict:
    prompt = f"""
You are an expert learning resource curator.

Rules:
- Output VALID JSON only
- No explanations or extra text
- Prefer free and open resources
- Match resources to roadmap phases
- Beginner-friendly content only

Schema:
{{
  "books": ["string"],
  "articles": ["string"],
  "videos": ["string"],
  "websites": ["string"],
  "tools": ["string"],
  "papers": ["string"],
  "difficulty_level": "string",
  "free_or_paid": "string"
}}

Concepts:
{json.dumps(concepts_output)}

Roadmap:
{json.dumps(roadmap_output)}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a resource recommendation engine. Output JSON only."
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
            "Resource Agent returned invalid JSON.\n"
            f"RAW OUTPUT:\n{raw}"
        ) from e
