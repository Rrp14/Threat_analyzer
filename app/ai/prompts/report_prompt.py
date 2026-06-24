import json


def build_report_prompt(
    context: dict,
) -> str:

    payload = json.dumps(
        context,
        indent=2,
    )

    return f"""
You are a senior cyber threat intelligence analyst.

Analyze the provided threat intelligence context.

Return ONLY valid JSON.

Schema:

{{
  "summary": "string",
  "analysis_overview": "string",
  "attack_scenario": "string",
  "business_impact": "string",

  "immediate_actions": [
    {{
      "title": "string",
      "description": "string",
      "priority": "low|medium|high|critical"
    }}
  ],

  "long_term_remediation": [
    {{
      "title": "string",
      "description": "string",
      "priority": "low|medium|high|critical"
    }}
  ],

  "monitoring": [
    {{
      "title": "string",
      "description": "string",
      "priority": "low|medium|high|critical"
    }}
  ]
}}

Threat Intelligence Context:

{payload}
"""