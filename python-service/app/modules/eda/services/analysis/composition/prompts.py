import json


def build_composition_prompt(
    question: str,
    composition_plan,
    evidence: dict,
    statistics: dict,
    chart: dict,
):
    return f"""
You are a Senior Data Analyst.

Your job is to explain composition findings to a non-technical business user.

You MUST ONLY use the supplied evidence.

Never invent numbers.

Never assume proportions that are not present.

--------------------------------------------------
USER QUESTION
--------------------------------------------------

{question}

--------------------------------------------------
COMPOSITION TYPE
--------------------------------------------------

{composition_plan.analysis_type}

--------------------------------------------------
CATEGORY
--------------------------------------------------

{composition_plan.category}

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
How is the whole broken down into parts?

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