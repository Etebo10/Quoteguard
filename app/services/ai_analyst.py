import json

from app.services.groq_client import client


MODEL = "openai/gpt-oss-120b"


def analyze_quote_with_ai(
    quote_data: dict,
    historical_evidence: dict | None = None,
) -> dict:

    if client is None:
        risk_count = len(quote_data.get("risks", []))
        pricing = quote_data.get("pricing", {})
        decision = "REVIEW" if risk_count else "APPROVE"
        return {
            "overall_assessment": (
                "QuoteGuard completed a deterministic financial review. "
                "AI analysis is unavailable because no Groq API key is configured."
            ),
            "confidence_score": 0.6,
            "pricing_assessment": (
                "The pricing model was calculated successfully, "
                f"with a recommended price of {pricing.get('recommended_price', 0):,.2f}."
            ),
            "key_concerns": [
                risk["message"] for risk in quote_data.get("risks", [])
            ],
            "recommendations": [
                risk["recommendation"] for risk in quote_data.get("risks", [])
            ] or [
                "Review the quote assumptions and confirm the expected margin before sending it."
            ],
            "decision": decision,
            "decision_reason": (
                "The quote was analyzed using the built-in pricing and risk logic; "
                "AI-based review remains unavailable in local/offline mode."
            ),
        }

    system_prompt = """
You are QuoteGuard's senior commercial quote analyst.

Your job is to analyze a proposed business quote using ONLY
the numerical calculations, historical evidence, and risks
provided to you.

You MUST NOT recalculate or invent financial figures.

You must:
1. Assess the commercial quality of the quote.
2. Identify important concerns.
3. Explain why those concerns matter.
4. Recommend practical actions.
5. Make a final decision.

Possible decisions:
- APPROVE
- REVIEW
- REJECT

Return only the requested structured JSON.
"""

    user_prompt = f"""
Analyze this QuoteGuard quote.

CURRENT QUOTE:

{json.dumps(quote_data, indent=2)}


HISTORICAL EVIDENCE:

{json.dumps(
    historical_evidence or {},
    indent=2
)}


IMPORTANT RULES:

- Do not invent facts.
- Do not invent historical data.
- Do not change the calculated price.
- Do not override Python calculations.
- Use historical evidence only when it is provided.
- Clearly distinguish historical evidence from assumptions.
- If there is insufficient historical evidence, say so.
"""

    response = client.chat.completions.create(
        model=MODEL,

        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],

        temperature=0,

        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "quote_analysis",
                "strict": True,
                "schema": {
                    "type": "object",

                    "properties": {
                        "overall_assessment": {
                            "type": "string"
                        },

                        "confidence_score": {
                            "type": "number"
                        },

                        "pricing_assessment": {
                            "type": "string"
                        },

                        "key_concerns": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },

                        "recommendations": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },

                        "decision": {
                            "type": "string",
                            "enum": [
                                "APPROVE",
                                "REVIEW",
                                "REJECT"
                            ]
                        },

                        "decision_reason": {
                            "type": "string"
                        }
                    },

                    "required": [
                        "overall_assessment",
                        "confidence_score",
                        "pricing_assessment",
                        "key_concerns",
                        "recommendations",
                        "decision",
                        "decision_reason"
                    ],

                    "additionalProperties": False
                }
            }
        }
    )

    content = response.choices[0].message.content

    return json.loads(content)