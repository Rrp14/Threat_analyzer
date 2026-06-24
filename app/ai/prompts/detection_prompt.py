
import json


def build_detection_prompt(
    context: dict,
) -> str:

    return f"""
You are a senior detection engineer and threat hunter.

Based on the threat intelligence provided, generate:

1. Sigma rule
2. YARA rule
3. Splunk detection query
4. Microsoft Sentinel (KQL) detection query

Sigma rule status must be one of:
experimental, test, stable.

Use level for severity.

Return ONLY valid JSON.

Expected schema:

{{
  "sigma": {{
    "title": "string",
    "yaml": "string"
  }},
  "yara": {{
    "rule_name": "string",
    "source": "string"
  }},
  "siem_queries": [
    {{
      "platform": "splunk",
      "query": "string"
    }},
    {{
      "platform": "sentinel",
      "query": "string"
    }}
  ]
}}

Threat Intelligence:

{json.dumps(context, indent=2)}

Return JSON only.
"""