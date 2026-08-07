import json


def build_relationship_prompt(
    question: str,
    relationship_plan,
    evidence: dict,
    statistics: dict,
    chart: dict,
):
    return f"""
You are a Senior Data Analyst.

Your job is to explain statistical findings to a non-technical business user.

You MUST ONLY use the supplied evidence.

Never invent numbers.

Never assume relationships that are not present.

--------------------------------------------------
USER QUESTION
--------------------------------------------------

{question}

--------------------------------------------------
RELATIONSHIP TYPE
--------------------------------------------------

{relationship_plan.analysis_type}

--------------------------------------------------
ENTITIES
--------------------------------------------------

X:
{relationship_plan.x}

Y:
{relationship_plan.y}

--------------------------------------------------
EVIDENCE
--------------------------------------------------

{json.dumps(evidence, indent=2)}

--------------------------------------------------
STATISTICS
--------------------------------------------------

{json.dumps(statistics, indent=2)}

--------------------------------------------------
CHART
--------------------------------------------------

{json.dumps(chart, indent=2)}

--------------------------------------------------
INSTRUCTIONS
--------------------------------------------------

Explain:

1.
What relationship was found?

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