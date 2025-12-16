import json
from backend.llm.client import client
from backend.utils.extract_first_json import extract_first_json

MODEL = "llama-3.1-8b-instant"
TEMPERATURE = 0.0


def debate_agent(topic: str, timeline_output: dict) -> dict:
    prompt = f"""
You are an expert analyst identifying key debates in a technical field.

Rules:
- Output VALID JSON only
- No explanations or text outside JSON
- Base debates on historical, present, and future tensions
- Debates must be relevant to learners and practitioners

Schema:
{{
  "debates": [
    {{
      "id": "string",
      "title": "string",
      "description": "string",
      "pro_arguments": ["string"],
      "con_arguments": ["string"],
      "status": "open | resolved | emerging",
      "created_at": "string (ISO 8601)",
      "updated_at": "string (ISO 8601)",
      "stakeholders": ["string"],
      "impact_level": "low | medium | high"
    }}
  ]
}}

Topic:
{topic}

Timeline:
{json.dumps(timeline_output)}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a debate synthesis engine. Output JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=TEMPERATURE,
        max_tokens=1500
    )

    raw = response.choices[0].message.content
    json_text = extract_first_json(raw)

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            "Debate Agent returned invalid JSON.\n"
            f"RAW OUTPUT:\n{raw}"
        ) from e
