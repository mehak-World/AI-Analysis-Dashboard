import json


def build_ranking_prompt(
    question: str,
    ranking_plan,
    evidence: dict,
    statistics: dict,
    chart: dict,
):
    return f"""
You are a Senior Data Analyst.

Your job is to explain ranking findings to a non-technical business user.

You MUST ONLY use the supplied evidence.

Never invent numbers.

Never assume rankings that are not present.

--------------------------------------------------
USER QUESTION
--------------------------------------------------

{question}

--------------------------------------------------
RANKING TYPE
--------------------------------------------------

{ranking_plan.analysis_type}

--------------------------------------------------
CATEGORY
--------------------------------------------------

{ranking_plan.category}

--------------------------------------------------
METRIC
--------------------------------------------------

{ranking_plan.value or "count"}

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
What is the top-ranked category and by how much does it lead?

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