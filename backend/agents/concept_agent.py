import json
from backend.llm.client import client
from backend.utils.extract_first_json import extract_first_json


MODEL = "llama-3.1-8b-instant"
TEMPERATURE = 0.0

def concept_agent(scope_output):
    prompt = f"""
You are an expert educational content creator.

Rules:
- Output VALID JSON only
- Follow this exact schema
- Do not include explanations, comments, or text outside the JSON object

Schema:
{{
  "concepts": [
    {{
      "name": "string",
      "description": "string",
      "related_concepts": ["string"],
      "constraints": {{
        "max_length": 0,
        "min_length": 0
      }},
      "difficulty_level": "string",
      "common_misconceptions": ["string"],
      "examples": [
        {{
          "example_description": "string",
          "code_snippet": "string"
        }}
      ]
    }}
  ]
}}

Topic Scope:
{json.dumps(scope_output, indent=2)}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a JSON generation engine. You must output valid JSON and nothing else."
            },
            {"role": "user", "content": prompt}
        ],
        temperature=TEMPERATURE,
        max_tokens=3000
    )

    concept_output = response.choices[0].message.content

    json_text = extract_first_json(concept_output)

    try:
        concept_data = json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            "Concept Agent returned invalid JSON.\n"
            f"RAW OUTPUT:\n{concept_output}"
        ) from e

    return concept_data
