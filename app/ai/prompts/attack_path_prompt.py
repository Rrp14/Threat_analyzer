def build_attack_path_prompt(
    context: dict,
) -> str:

    return f"""
You are a senior threat hunter.

Based on the threat intelligence below:

{context}

Predict the most likely attacker progression.

Return ONLY valid JSON.

Rules:
- confidence must be a decimal between 0.0 and 1.0
- stages must be an array
- technique_id must be a valid MITRE ATT&CK technique ID
- do not include markdown
- do not include explanations outside JSON

Example:

{{
  "confidence": 0.95,
  "stages": [
    {{
      "stage": "Initial Access",
      "technique_id": "T1190",
      "description": "Exploit public facing application",
      "confidence": 0.90
    }},
    {{
      "stage": "Command and Control",
      "technique_id": "T1071",
      "description": "Establish outbound C2 communication",
      "confidence": 0.85
    }}
  ]
}}
"""