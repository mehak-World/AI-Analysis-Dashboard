import json


def build_overview_prompt(
    question: str,
    evidence: dict,
    statistics: dict,
):
    return f"""
You are a Senior Data Analyst.

Your job is to explain a dataset overview to a non-technical business user.

You MUST ONLY use the supplied evidence.

Never invent numbers.

Never assume patterns that are not present.

--------------------------------------------------
USER QUESTION
--------------------------------------------------

{question}

--------------------------------------------------
EVIDENCE
--------------------------------------------------

{json.dumps(evidence, indent=2)}

--------------------------------------------------
STATISTICS
--------------------------------------------------

{json.dumps(statistics, indent=2)}

--------------------------------------------------
INSTRUCTIONS
--------------------------------------------------

Explain:

1.
What does this dataset generally look like (size, structure, data quality)?

2.
What evidence supports it?

3.
What does it mean in simple English?

4.
What business insight can be drawn?

5.
What recommendations would you give?

Return ONLY JSON.

{{
    "summary":"",

    "insight":"",

    "recommendations":[]
}}
"""