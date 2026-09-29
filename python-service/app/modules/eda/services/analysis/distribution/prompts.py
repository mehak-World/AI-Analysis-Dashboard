import json


def build_distribution_prompt(
    question: str,
    distribution_plan,
    evidence: dict,
    statistics: dict,
    chart: dict,
):
    return f"""
You are a Senior Data Analyst.

Your job is to explain statistical findings to a non-technical business user.

You MUST ONLY use the supplied evidence.

Never invent numbers.

Never assume patterns that are not present.

--------------------------------------------------
USER QUESTION
--------------------------------------------------

{question}

--------------------------------------------------
DISTRIBUTION TYPE
--------------------------------------------------

{distribution_plan.analysis_type}

--------------------------------------------------
COLUMN
--------------------------------------------------

{distribution_plan.column}

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
What does the distribution of this column look like?

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